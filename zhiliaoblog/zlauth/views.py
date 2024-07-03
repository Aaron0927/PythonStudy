from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import random
import string
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout

# 获取 admin 里面的 User 模型
User = get_user_model()

# Create your views here.
@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            print(remember)
            user = User.objects.filter(email=email).first()
            # 用户存在，且密码正确
            if user and user.check_password(password):
                # 登录
                login(request, user)
                # 判断是否有记住我
                if not remember:
                    # 修改 session 的到期时间,到期时间为 0 表示关闭浏览器后就会删除 session
                    request.session.set_expiry(0)
                # 重定向到首页
                return redirect('/')
            else:
                print('邮箱或密码错误！')
                # 重新刷新登录页面
                return redirect(reverse('zlauth:login'))

def zllogout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 验证成功后从表单中获取数据
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')
            User.objects.create_user(username=username, email=email, password=password)
            # 重定向到登录页面
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            # 重新加载注册页面
            return redirect(reverse('zlauth:register'))


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": "必须传递邮箱!"})
    # 随机 4 位数字验证码
    captcha = "".join(random.sample(string.digits, k=4))
    # 保存在数据库
    # 根据 email 查找，找到就更新captcha，否则就用 email 和captcha创建数据
    CaptchaModel.objects.update_or_create(email=email, defaults={"captcha": captcha})
    send_mail(subject="知了博客注册验证码", message=f"您的注册验证码是{captcha}", from_email=None,
              recipient_list=[email], fail_silently=False)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功!"})
