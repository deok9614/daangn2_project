from django.urls import path, include
from django.contrib import admin
from . import views
# from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
app_name = 'dangun_app'

=======
>>>>>>> js
urlpatterns = [
    path('', views.login, name='login'), # 메인 페이지
    path('chat/', views.chat, name='chat'),
    path('location/', views.location, name='location'),
    path('login/', views.login, name='location'),
    path('trade/', views.trade, name='trade'),
    path('trade_post/', views.trade_post, name='trade_post'),
    path('trade_post/<int:product_id>/',views.trade_post, name='trade_post_id'),
    path('write/', views.write, name='write'),
    path('main/', views.main, name='main'),
<<<<<<< HEAD
    path('write/<int:product_id>/edit', views.write, name='edit'),
=======
    path('register/', views.register, name='register'),  # 'register' URL 패턴 정의
>>>>>>> js
]