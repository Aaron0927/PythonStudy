from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='分类名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='博客标题')
    content = models.TextField(verbose_name='博客内容')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='博客分类')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        # 指定排序字段
        ordering = ['-pub_time']

class BlogComment(models.Model):
    # blog 和 comment 直接属于 1 对多的关系，增加反向指定 -> 通过 blog 获取到 comments
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name='博客')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    comment = models.TextField(verbose_name='评论')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name
        # 指定排序字段
        ordering = ['-pub_time']
