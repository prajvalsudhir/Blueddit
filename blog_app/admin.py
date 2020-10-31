from django.contrib import admin
from .models import post,comment,userinfo
# Register your models here.

admin.site.register(post)
admin.site.register(comment)
admin.site.register(userinfo)
# admin.site.register(like)
# super user info:
# username = prajval
# email=prajvalsudhir@gmail.com
# password=pscarmel