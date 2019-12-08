__author__ = "lishuntao"
__date__ = "2019/11/3 0003 17:53"
from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentsView



urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    #课程章节信息
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentView.as_view(), name="course_comments"),
    #添加评论啊
    url(r'^add_comment/', AddCommentsView.as_view(), name="add_comment"),

]