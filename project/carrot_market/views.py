from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Post
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
def trade_post(request):
    return render(request, 'dangun_app/trade_post.html')

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
        if form.is_valid():
            # 아이디 생성 시 주석 제거
            # post.user_id = request.user.username
            post = form.save()
            return redirect('dangun_app:trade_post')
    
    context = {'form': form}
    return render(request,'dangun_app/write.html' , context)



def main(request):
    return render(request, 'dangun_app/main.html')