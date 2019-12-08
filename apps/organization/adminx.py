__author__ = "lishuntao"
__date__ = "2019/10/30 0030 16:29"

import xadmin

from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):
    list_display = ["name","desc","add_time"]
    search_fields = ["name","desc"]
    list_filter = ["name","desc","add_time"]
    model_icon = "fa fa-map-marker"

class CourseOrgAdmin(object):
    list_display = ["name", "desc", "click_nums","fav_nums","address","city","add_time"]
    search_fields = ["name", "desc", "click_nums","fav_nums","address","city"]
    list_filter = ["name", "desc", "click_nums","fav_nums","address","city","add_time"]
    #给选择课程的机构外键的模型类添加搜索，当数据量过大可以不用全部加载出来
    # relfield_style = "fk-ajax"
    model_icon = "fa fa-building"

class TeacherAdmin(object):
    list_display = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums","fav_nums","add_time"]
    search_fields = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums","fav_nums"]
    list_filter = ["org", "name", "work_years", "work_company", "work_position", "points", "click_nums","fav_nums","add_time"]
    model_icon = "fa fa-tachometer"

xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)