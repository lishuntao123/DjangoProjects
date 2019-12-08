# -*- coding: gbk -*-

import json
from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
# Create your views here.

class CustomBackend(ModelBackend):
    #这个验证类会自动调用这个方法，要在settings中注册,（目的用其他验证方式）
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            #模型类中的过滤条件 或(|)语句 需要用到Q查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #因为密码是加密的，因此模型类对象提供的验证密码的方法，参数是密码
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, "login.html")
        else:
            return render(request,"active_failed.html")


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form":register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")
            pass_word = request.POST.get("password","")

            if UserProfile.objects.filter(email=user_name):
                print(user_name, pass_word)
                return render(request, "register.html", {"msg": "此账号已经激活！","register_form":register_form})

            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()
            #写入注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕课网"
            user_message.save()
            send_register_email(user_name,"register")
            return render(request, "register.html", {"msg": "邮件已经发送啦！"})
        else:
            return render(request, "register.html",{"register_form":register_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self,request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))



class LoginView(View):
    def get(self,request):
        return render(request, "login.html", {})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 然后验证账号密码
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html",{"msg":"未激活状态！"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form})

#因为视图都希望用类来做视图#####LoginView##########
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         #然后验证账号密码
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request, "login.html", {"msg":"用户名或密码错误！"})
#     elif request.method == "GET":
#         return render(request,"login.html",{})


class ForgetPwdView(View):
    def get(self,request):
        #实例化向模板传入实例化对象 加载验证码图片
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email, "forget")
            return render(request,"send_success.html")
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html",{"email":email})
        else:
            return render(request, "active_failed.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self,request):
        email = request.POST.get("email", "")
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email,"msg":"两次密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        return render(request, "password_reset.html", {"email": email,"modify_form":modify_form})


class UserInfoView(LoginRequiredMixin,View):
    """
    用户个人信息,必须登录才能访问
    """
    def get(self,request):
        return render(request,"usercenter-info.html",{})

    def post(self,request):
        #一定要告诉是哪一个实例，不然会新增一条记录
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin,View):
    """
    用户修改头像
    """
    def post(self,request):
        #添加第三个参数就让它拥有model.Form的功能（实例的意思）
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data["image"]
            #上面世界传入实例参数，就不用了实例化image对象直接可以保存
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail"}', content_type="application/json")


class UpdatePwdView(View):
    """
    在个人中心修改密码
    """
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success","msg":"密码修改成功"}', content_type="application/json")
        return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class SendEmailCodeView(LoginRequiredMixin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get("email","")

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经注册"}', content_type="application/json")
        print("daozhelila")
        send_register_email(email, "update_email")
        print("来啦来啦")
        return HttpResponse('{"status":"success","msg":"发送成功"}', content_type="application/json")


class UpdateEmailView(LoginRequiredMixin,View):
    """
    修改验证码
    """
    def post(self,request):
        email = request.POST.get("email","")
        code = request.POST.get("code","")
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type="application/json")


class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_course = UserCourse.objects.filter(user=request.user)

        return render(request,"usercenter-mycourse.html",{
            "user_course":user_course,
        })



class MyfavOrgView(LoginRequiredMixin,View):
    """
    我收藏的课程 机构
    """
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,"usercenter-fav-org.html",{
            "org_list":org_list,
        })


class MyfavTeacherView(LoginRequiredMixin,View):
    """
    我收藏的授课讲师
    """
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request,"usercenter-fav-teacher.html",{
            "teacher_list":teacher_list,
        })



class MyfavCourseView(LoginRequiredMixin,View):
    """
    我收藏的课程
    """
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request,"usercenter-fav-course.html",{
            "course_list":course_list,
        })


class MymessageView(LoginRequiredMixin,View):
    """
    我的消息
    """
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        #用户进入个人消息将未读消息设置成已经读取
        all_unread_messges = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messges:
            unread_message.has_read = True
            unread_message.save()
        # 对个人消息进行分页
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 10, request=request)
        messages = p.page(page)
        return render(request,"usercenter-message.html",{
            "messages":messages,
        })


class IndexView(View):
    """
    在线网首页
    """
    def get(self,request):
        #1、取出轮播图
        all_banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,"index.html",{
            "all_banners":all_banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs,
        })

def page_not_found(request):
    """
    全局404页面处理函数
    :param request:
    :return:
    """
    # from django.shortcuts import render_to_response
    response = render_to_response("404.html",{})
    response.status_code = 404
    return response


def page_error(request):
    """
    全局500页面处理函数
    :param request:
    :return:
    """
    response = render_to_response("500.html",{})
    response.status_code = 500
    return response