"""day16 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app01.views import depart, user, pretty,place,room,seat,reservation,login
from app01.views.interface import login_page,home_page,seat_page,complete_reservation,sign_in_page,my_page,reservation_page

urlpatterns = [
    # path('admin/', admin.site.urls),

    #登录
    path('', login.login_view, name='login'),  # 设置 '' 为登录视图

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:nid>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/form/add/', user.user_model_form_add),
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 靓号管理
    path('pretty/list/', pretty.pretty_list),
    path('pretty/add/', pretty.pretty_add),
    path('pretty/<int:nid>/edit/', pretty.pretty_edit),
    path('pretty/<int:nid>/delete/', pretty.pretty_delete),

    # 场所管理
    path('place/list/', place.place_list),
    path('place/add/', place.place_add),
    path('place/<int:nid>/edit/', place.place_edit),
    path('place/<int:nid>/delete/', place.place_delete),

    # 自习室管理
    path('room/list/', room.room_list),
    path('room/add/', room.room_add),
    path('room/<int:nid>/edit/', room.room_edit),
    path('room/<int:nid>/delete/', room.room_delete),

    # 预约记录管理
    path('reservation/list/', reservation.reservation_list),
    path('reservation/add/', reservation.reservation_add),
    path('reservation/<int:nid>/edit/', reservation.reservation_edit),
    path('reservation/<int:nid>/delete/', reservation.reservation_delete),

    # 座位管理
    path('seat/list/', seat.seat_list),
    path('seat/add/', seat.seat_add),
    path('seat/<int:nid>/edit/', seat.seat_edit),
    path('seat/<int:nid>/delete/', seat.seat_delete),

    #登录逻辑处理
    path('login_page/', login_page, name='login_page'),

    #首页逻辑处理
    path('home_page/', home_page, name='home_page'),

    #座位页面的逻辑处理
    path('seat_page/', seat_page, name='seat_page'),

    #完成预约的逻辑操作
    path('complete_reservation/', complete_reservation, name='complete_reservation'),
    
    #完成签到的逻辑操作
    path('sign_in_page/', sign_in_page, name='sign_in_page'),

    #我的页面的逻辑操作
    path('my_page/', my_page, name='my_page'),

    #查看预约的逻辑操作
    path('reservation_page/', reservation_page, name='reservation_page'),
]
