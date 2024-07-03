from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '请传入用户名！',
        'min_length': '用户名长度在2～20之间！',
        'max_length': '用户名长度在2～20之间！',
    })
    email = forms.EmailField(error_messages={
        'required': '请输入邮箱！',
        'invalid': '请输入正确的邮箱！',
    })
    captcha = forms.CharField(min_length=4, max_length=4)
    password = forms.CharField(min_length=6, max_length=20)

    # 添加对 email 的验证
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 判断 email 是否在数据库中已经存在
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已经被注册！')
        return email

    # 添加对验证码的验证
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        # 获取验证码对象
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('邮箱和验证码不匹配！')
        # 验证完后删除验证码
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={
        'required': '请输入邮箱！',
        'invalid': '请输入正确的邮箱！',
    })
    password = forms.CharField(min_length=6, max_length=20)
    remember = forms.IntegerField(required=False)
