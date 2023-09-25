from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Post, User
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request,'registration/login.html')
def chat(request):
    return render(request, 'dangun_app/chat.html')
def location(request):
    pass
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