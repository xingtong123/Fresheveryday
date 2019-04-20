from django.contrib import admin
from .models import Userext,Category,Goods,Cart,Orderinfo,Ordergoods
# from django.contrib.auth.models import User
# Register your models here.
admin.site.register([Userext,Category,Goods,Cart,Orderinfo,Ordergoods])
# admin.site.register(User)