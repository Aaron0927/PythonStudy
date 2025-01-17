from django.db import models

# Create your models here.
class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)