from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  #  폼 객체를 생성하고, 이 폼 객체를 템플릿에 "form" 변수로 전달

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)  # AuthenticationForm 객체 생성
        if form.is_valid():  # 폼 유효성 검사
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:  # 사용자가 인증되었을 때만
                login(request, user)  # 로그인 함수에 사용자 객체를 전달합니다.
                return HttpResponse("로그인 성공!")
            else:
                return HttpResponse("로그인 실패!")
    else:
        form = AuthenticationForm()  # GET 요청 시 폼 생성
    return render(request, 'registration/login.html', {"form": form})  # 폼을 템플릿에 전달

def register(request):
    return render(request,'registration/register.html')

def chat(request):
    pass
def location(request):
    pass
def trade(request):
    pass
def trade_post(request):
    pass
def write(request):
    return render(request, 'dangun_app/write.html')
def main(request):
    return render(request, 'dangun_app/main.html')