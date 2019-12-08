__author__ = "lishuntao"
__date__ = "2019/11/10 0010 22:26"

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


#excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        """
        确定是否加载我们的插件
        :param args:
        :param kwargs:
        :return:true或者false   true加载插件
        """
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        """
        将我们的html文件代码显示在top_toolbar顶部工具栏上
        :param context:
        :param nodes:
        :return:
        """
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html', context_instance=context))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)