__author__ = "lishuntao"
__date__ = "2019/10/30 0030 15:54"

import xadmin

from .models import Course,Lesson,Video,CourseResource,BannerCourse
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ["name", "desc", "detail", "degree","learn_times","students","fav_nums","image","click_nums","add_time","get_zj_nums","go_to"]
    search_fields = ["name", "desc", "detail", "degree","learn_times","students","fav_nums","click_nums"]
    list_filter = ["name", "desc", "detail", "degree","learn_times","students","fav_nums","image","click_nums","add_time",]
    ordering = ["-click_nums"]
    list_editable = ["degree","desc"]
    readonly_fields = ["click_nums"]
    #在管理后台隐藏字段  他与仅仅可看冲突
    exclude = ["fav_nums"]
    model_icon = "fa fa-book"
    #只能做一级嵌套，目的就是为了更便利添加数据
    inlines = [LessonInline,CourseResourceInline]
    style_fields = {"detail": "ueditor"}
    #会覆盖掉excel插件中的那个变量
    import_excel = True
    #在这里重写queryset方法 达到我们想要的过滤，以及多个管理目录对一张表的管理
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs
    #每3秒刷新一次 让用户选择几秒刷新
    refresh_times = [3,5]
    #当某些数据发生变化的时候，我们需要进行一些操作 重载admin中的save_models方法
    def save_models(self):
        """
        在保存课程的时候 统计的课程数自动保存在模型类机构数据表的课程数中
        :return:
        """
        obj = self.new_obj
        #当前课要先保存起来 不然下面查询就少一个课程数
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request,args,kwargs)


class BannerCourseAdmin(object):
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image","click_nums", "add_time", ]
    search_fields = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "click_nums"]
    list_filter = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums","add_time", ]
    ordering = ["-click_nums"]
    readonly_fields = ["click_nums"]
    # 在管理后台隐藏字段  他与仅仅可看冲突
    exclude = ["fav_nums"]
    model_icon = "fa fa-book"
    # 只能做一级嵌套，目的就是为了更便利添加数据
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ["course","name","add_time",]
    search_fields = ["course","name","add_time",]
    list_filter = ["course__name","name","add_time",]
    model_icon = "fa fa-pencil-square-o"


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time", ]
    search_fields = ["lesson", "name"]
    list_filter = ["lesson", "name", "add_time", ]
    model_icon = "fa fa-file-video-o"


class CourseResourceAdmin(object):
    list_display = ["course", "name", "download","add_time"]
    search_fields = ["course", "name","download"]
    list_filter = ["course", "name", "download","add_time"]
    model_icon = "fa fa-map"


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

