__author__ = "lishuntao"
__date__ = "2019/11/2 0002 9:50"
import re
from django import forms


from operation.models import UserAsk

# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,min_length=5,max_length=50)

#forms.ModelForm很强大，直接完成了forms.Form的功能，还能添加额外的验证字段
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk#这是指定那个模型类表单验证
        fields = ['name','mobile','course_name']#指定那些字段验证
    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data["mobile"]
        REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法",code="mobile_invalid")
