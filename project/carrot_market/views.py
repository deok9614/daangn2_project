from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  #  폼 객체를 생성하고, 이 폼 객체를 템플릿에 "form" 변수로 전달
from .models import Post, User
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

def search(request):
    return render(request, 'dangun_app/trade.html')

def trade(request):
    top_views_posts = Post.objects.filter(product_sold='N').order_by('-views')
    return render(request, 'dangun_app/trade.html', {'posts': top_views_posts})

def trade_post(request, product_id=None):
    post = get_object_or_404(Post, pk=product_id)

    # 쿠키 데이터를 이용 - 새로고침 시 조회수 늘어나지 않음
    cookie_name = f'main_{product_id}_viewed'
    if cookie_name not in request.COOKIES:
        post.views += 1
        post.save()
        # 조회수 증가 막는 기간 : 하루
        expires = datetime.now() + timedelta(days=1)
        expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
        response = render(request, 'dangun_app/trade_post.html', {'post': post})
        response.set_cookie(cookie_name, 'true', expires=expires)
        return response
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
def write(request, product_id = None):
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
    top_views_posts = Post.objects.filter(product_sold='N').order_by('-views')[:8]
    return render(request, 'dangun_app/main.html', {'posts': top_views_posts})


# test 중 - 신지수
# @login_required
# def write(request, product_id=None):
#     if request.method == "POST":
        # if form.is_valid():
        #     # 아이디 생성 시 주석 제거
        #     # post.user_id = request.user.username
        #     post = form.save()
        #     product_id = post.product_id
        #     return redirect('dangun_app:trade_post', product_id=product_id)
#         else:
#             try:
#                 user_profile = User.objects.get(user_id=request.user.username)
#                 if user_profile.location:
#                     form = PostForm()
#                 else:
#                     messages.error(request, '동네인증이 필요합니다.')
#                     return redirect('dangun_app:alert', alert_message='동네인증이 필요합니다.')
#             except User.DoesNotExist:
#                 messages.error(request, '동네인증이 필요합니다.')
#                 return redirect('dangun_app:alert', alert_message='동네인증이 필요합니다.')
    
#     context = {'form': form}
#     return render(request, 'dangun_app/write.html', context)