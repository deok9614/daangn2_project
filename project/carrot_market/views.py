from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Post
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone
def login(request):
    pass
def chat(request):
    pass
def location(request):
    pass
def trade(request):
    pass
def trade_post(request):
    pass

# @login_required
def write(request, product_id=None):
    # 업로드
    if request.method == 'POST':
        form = PostForm(request.POST) # 폼 초기화
        if form.is_valid():
            post = form.save(using='daangn2')
            return redirect('carrot_market:trade_post', product_id=post.product_id)
    # 폼을 초기화함
    else:
        form = PostForm()

    context = {'form': form, 'MEDIA_URL': settings.MEDIA_URL,}
    return render(request,'dangun_app/write.html' , context)

def main(request):
    return render(request, 'dangun_app/main.html')