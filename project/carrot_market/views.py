from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm  #  폼 객체를 생성하고, 이 폼 객체를 템플릿에 "form" 변수로 전달
from .models import Post, UserProfile, PostImage, ChatRoom, Message
from .forms import PostForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.db.models import Q
from .forms import PostForm, CustomLoginForm, CustomUserForm

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dangun_app:main')
    else:
        form = CustomLoginForm(data=request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    print(form.errors)
                    login(request, user)
                    return redirect('dangun_app:main')
                else:
                    print(form.errors)
                    return HttpResponse("로그인 실패!")
        else:
            form = CustomLoginForm()
        return render(request, 'registration/login.html', {'form': form})
    
def register(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 == password2:
                user.user = form.cleaned_data['username']
                user.password = form.cleaned_data['password1']
                user.save()
            # login(request, user)
            return redirect('dangun_app:main')
    else:
        form = CustomUserForm()

    return render(request, 'registration/register.html', {'form': form})

def chat(request):
    return render(request, 'dangun_app/chat.html')

    return render(request, 'dangun_app/chat.html')

def location(request):
    return render(request, 'dangun_app/location.html') 

def search(request):
    return render(request, 'dangun_app/trade.html')

def trade(request):
    top_views_posts = Post.objects.filter(product_sold='N').order_by('-views')
    return render(request, 'dangun_app/trade.html', {'posts': top_views_posts})

def trade_post(request, product_id=None, post_id=None):
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
        user_profile = UserProfile.objects.get(user_id=post.user_id)
    except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'post': post,
        'user_profile': user_profile,
    }

    return render(request, 'dangun_app/trade_post.html', context)

# @login_required
def write(request, product_id = None, user_id=None):
    post = None
    form = PostForm(request.POST)
    image_form = PostImage(request.FILES.getlist("image"))
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            # post.user_id = request.user.user_id

            post = form.save()
    
            for image in request.FILES.getlist("image"):
                image_form = PostImage(post_id=post.pk, image=image)
                image_form.save()

            product_id = post.product_id
            return redirect('dangun_app:trade_post', product_id=product_id)

    
    context = {'form': form}
    return render(request,'dangun_app/write.html' , context)

def edit(request, product_id=None):
    post = None
    if product_id:
        post = get_object_or_404(Post, product_id=product_id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)

            post.title = request.POST['title']
            post.price = request.POST['price']
            post.product_description = request.POST['product_description']
            post.deal_location = request.POST['deal_location']

            post.save()

            if request.FILES:
                PostImage.objects.filter(post=post).delete()
                for image in request.FILES.values():
                    PostImage.objects.create(
                        post=post,
                        image=image)

            return redirect('dangun_app:trade_post', product_id=product_id)
    else:  # GET 요청인 경우
        form = PostForm(instance=post)

    return render(request,'dangun_app/write.html' , {'post':post,'form': form})
        
def main(request):
    top_views_posts = Post.objects.filter(product_sold='N').order_by('-views')[:8]
    return render(request, 'dangun_app/main.html', {'posts': top_views_posts})


from django.contrib.auth.models import User

from django.contrib.auth import login
from django.shortcuts import render, redirect

from django.utils.decorators import method_decorator
from django.views import View


def chat_room_test(request):
    return render(request, 'dangun_app/chat_room.html')

def chat_room(request, pk):
    user = request.user
    chat_room = get_object_or_404(ChatRoom, pk=pk)

    # 내 ID가 포함된 방만 가져오기
    chat_rooms = ChatRoom.objects.filter(
            Q(receiver_id=user) | Q(starter_id=user)
        ).order_by('-latest_message_time')  # 최신 메시지 시간을 기준으로 내림차순 정렬
    
    # 각 채팅방의 최신 메시지를 가져오기
    chat_room_data = []
    for room in chat_rooms:
        latest_message = Message.objects.filter(chatroom=room).order_by('-timestamp').first()
        if latest_message:
            chat_room_data.append({
                'chat_room': room,
                'latest_message': latest_message.content,
                'timestamp': latest_message.timestamp,
            })

    # 상대방 정보 가져오기
    if chat_room.receiver == user:
        opponent = chat_room.starter
    else:
        opponent = chat_room.receiver

    opponent_user = UserProfile.objects.get(pk=opponent.pk)


    # post의 상태 확인 및 처리
    if chat_room.post is None:
        seller = None
        post = None
    else:
        seller = chat_room.post.user
        post = chat_room.post

    return render(request, 'dangun_app/chat_room.html', {
        'chat_room': chat_room,
        'chat_room_data': chat_room_data,
        'room_name': chat_room.pk,
        'seller': seller,
        'post': post,
        'opponent': opponent_user,
    })


# 채팅방 생성 또는 참여
def create_or_join_chat(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    chat_room = None
    created = False

    # 채팅방이 이미 존재하는지 확인
    chat_rooms = ChatRoom.objects.filter(
        Q(starter=user, receiver=post.user, post=post) |
        Q(starter=post.user, receiver=user, post=post)
    )
    if chat_rooms.exists():
        chat_room = chat_rooms.first()
    else:
        # 채팅방이 존재하지 않는 경우, 새로운 채팅방 생성
        chat_room = ChatRoom(starter=user, receiver=post.user, post=post)
        chat_room.save()
        created = True

    return JsonResponse({'success': True, 'chat_room_id': chat_room.pk, 'created': created})