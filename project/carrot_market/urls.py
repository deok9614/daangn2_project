from django.urls import path, include
from django.contrib import admin
from . import views
# from rest_framework.routers import DefaultRouter

app_name = 'dangun_app'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('location/', views.location, name='location'),
    path('login/', views.custom_login, name='login'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/<int:product_id>/',views.trade_post, name='trade_post'),
    path('write/', views.write, name='write'),
    path('', views.main, name='main'),# 메인 페이지 변경
    path('write/<int:product_id>/edit', views.edit, name='edit'),
    path('register/', views.register, name='register'),
    path('chat_room/<int:pk>/', views.chat_room, name='chat_room'),
    path('chat_room/', views.chat_room_test, name='chat_room'),
]