from django.contrib import admin
from .models import BlogCategory, Blog, BlogComment

# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'category', 'author', 'pub_time']

class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'author', 'comment']

admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogComment, BlogCommentAdmin)