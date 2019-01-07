# -*- coding: utf-8 -*-
# @Time    : 2019/1/5  10:15
# @Author  : zhangxinxin
# @Email   : 778786617@qq.com
# @Software: PyCharm
from django.urls import path
from . import views


app_name = 'jd'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<str:s_id>', views.detail, name='detail'),
    path('show_svg/<str:s_id>', views.show_svg, name='show_svg')
]

