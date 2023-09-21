from django.urls import path, include
from django.contrib import admin
from . import views
# from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', views.login, name='login'), # 메인 페이지
    path('chat/', views.chat, name='chat'),
    path('location/', views.location, name='location'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/', views.trade_post, name='trade_post'),
]