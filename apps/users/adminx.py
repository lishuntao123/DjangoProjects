__author__ = "lishuntao"
__date__ = "2019/10/30 0030 15:03"

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import EmailVerifyRecord,Banner,UserProfile

#如果需要定制页面，那么就自己重写函数
# class UserProfileAdmin(UserAdmin):
#     pass


class BaseSetting(object):
    """使用xadmin主题，默认是False"""
    enable_themes = True
    #开启bootstrap主题样式库
    use_bootswatch = True

class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    list_display = ["code","email","send_type","send_time"]
    search_fields = ["code","email","send_type"]
    list_filter = ["code","email","send_type","send_time"]
    model_icon = 'fa fa-envelope-open'


class BannerAdmin(object):
    list_display = ["title", "image", "url", "index","add_time"]
    search_fields = ["title", "image", "url", "index"]
    list_filter = ["title", "image", "url", "index","add_time"]
    model_icon = "fa fa-picture-o"
from django.contrib.auth.models import User
#卸载原来xadmin自动注册的权限下的用户  (这个bug已经修复了)
# xadmin.site.unregister(User)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
#在管理用户权限的用户将我们重写的用户信息注册进来（这个bug已经被修复了）
# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
