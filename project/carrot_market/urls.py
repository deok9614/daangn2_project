from django.urls import path, include
from django.contrib import admin
from . import views
# from rest_framework.routers import DefaultRouter

app_name = 'dangun_app'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('location/', views.location, name='location'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:product_id>/',views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),
    path('', views.main, name='main'),# 메인 페이지 변경
    path('write/<int:product_id>/edit', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    
    path('chat/', views.chat_view, name='chat'),
    path('chat_room/<int:pk>/', views.chat_room, name='chat_room'),
    path('chat_room/', views.chat_room_test, name='chat_room'),
    path('create_or_join_chat/<int:pk>/', views.create_or_join_chat, name='create_or_join_chat'),
    path('get_latest_chat/', views.get_latest_chat_no_pk, name='get_latest_chat_no_pk'),
    path('get_latest_chat/<int:pk>/', views.get_latest_chat, name='get_latest_chat'),

    path('confirm_deal/<int:post_id>/', views.ConfirmDealView.as_view(), name='confirm_deal'),
    
]