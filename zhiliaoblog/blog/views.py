from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import BlogCategory, Blog, BlogComment
from .forms import PubBlogForm
from  django.db.models import Q

# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, template_name='index.html', context={'blogs': blogs})

def blog_detail(request, blog_id: int):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        blog = None
    return render(request, template_name='blog_detail.html', context={'blog': blog})

# @login_required(login_url='/auth/login')
# @login_required(login_url=reverse_lazy('zlauth:login'))
@require_http_methods(['GET', 'POST'])
@login_required()
def pub_blog(request):
    if request.method == 'GET':
        categories = BlogCategory.objects.all()
        return render(request, template_name='pub_blog.html', context={"categories": categories})
    else:
        form = PubBlogForm(request.POST)
        print(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            blog = Blog.objects.create(title=title, content=content, category_id=category_id, author=request.user)
            return JsonResponse({"code": 200, "message": "博客发布成功！", "data": {"blog_id": blog.id}})
        else:
            print(form.errors)
            return JsonResponse({"code": 400, "message": "发布博客失败！"})

# 发布评论
@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get('blog_id')
    comment = request.POST.get('content')
    BlogComment.objects.create(blog_id=blog_id, comment=comment, author=request.user)
    # 重定向到blog 详情页
    return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))


# 查询请求
@require_GET
def blog_search(request):
    # search?q=xxx
    q = request.GET.get('q')
    # 不区分大小写，title 或 content 中包含 q
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, template_name='index.html', context={'blogs': blogs})
