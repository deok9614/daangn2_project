from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  #  폼 객체를 생성하고, 이 폼 객체를 템플릿에 "form" 변수로 전달
from .models import Post, User
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
    return render(request, 'dangun_app/chat.html')

def location(request):
    return render(request, 'dangun_app/location.html') 

def trade(request):
    pass
def trade_post(request, product_id=None):
    post = get_object_or_404(Post, product_id=product_id)

    # 조회수 증가
    if request.user.is_authenticated:
        if request.user != post.user:
            post.views += 1
            post.save()
    else:
        post.views += 1
        post.save()

    try:
        user_profile = User.objects.get(user_id=post.user_id)
    except User.DoesNotExist:
            user_profile = None

    context = {
        'post': post,
        'user_profile': user_profile,
    }

    return render(request, 'dangun_app/trade_post.html', context)

# @login_required
def write(request, product_id=None):
    # 수정
    if product_id:
        post = get_object_or_404(Post, id=product_id)
        
    # 폼을 초기화함
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
        else:
            form = PostForm(instance=post)
    else:
        post = None
        form = PostForm(request.POST, request.FILES)
    if request.method == "POST":
        print(form.errors)
        if form.is_valid():
            # 아이디 생성 시 주석 제거
            # post.user_id = request.user.username
            post = form.save()
            product_id = post.product_id
            return redirect('dangun_app:trade_post', product_id=product_id)
    
    context = {'form': form}
    return render(request,'dangun_app/write.html' , context)



def main(request):
    return render(request, 'dangun_app/main.html')