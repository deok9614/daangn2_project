from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  #  폼 객체를 생성하고, 이 폼 객체를 템플릿에 "form" 변수로 전달
from .models import Post, User
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, UserProfile, PostImage
from .forms import PostForm, CustomLoginForm, CustomUserForm
from django.contrib import messages
from social_core.backends.google import GoogleOAuth2
from social_core.backends.naver import NaverOAuth2

def logout_user(request):
    logout(request)
    return redirect('/')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dangun_app:main')
    else:
        form = CustomLoginForm(data=request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # 사용자가 선택한 로그인 백엔드를 가져옵니다.
                backend = request.POST.get('login_with')

                # 선택한 백엔드에 따라 사용자를 인증합니다.
                if backend == 'google':
                    user = authenticate(request, backend=GoogleOAuth2.name)
                elif backend == 'naver':
                    user = authenticate(request, backend=NaverOAuth2.name)
                else:
                    user = authenticate(request, username=username, password=password)

                if user is not None:
                    # 수정 중!!
                    login(request, user)
                    return redirect('dangun_app:main')
                else:
                    return HttpResponse("로그인 실패!")
        return render(request, 'registration/login.html', {'form': form})

def register(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            error_message = "이미 존재하는 아이디입니다."
        elif form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dangun_app:main')
            else:
                form.add_error('password2', '비밀번호가 일치하지 않습니다')
    else:
        form = CustomUserForm()

    return render(request, 'registration/register.html', {'form': form, 'error_message': error_message})
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

def edit(request, product_id):
    post = get_object_or_404(Post, product_id=product_id)
    if product_id:
        post.product_description = post.product_description.strip()
        if request.method == "POST":
            post.title = request.POST['title']
            post.price = request.POST['price']
            post.product_description = request.POST['product_description']
            post.deal_location = request.POST['deal_location']
            if 'product_img' in request.FILES:
                post.product_img = request.FILES['product_img']
            post.save()
            return redirect('dangun_app:trade_post', product_id=product_id)
        return render(request,'dangun_app/write.html' , {'post':post})

def main(request):
    return render(request, 'dangun_app/main.html')