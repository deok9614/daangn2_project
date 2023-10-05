from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Post, UserProfile, PostImage, ChatRoom, Message
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm, CustomLoginForm, CustomUserForm
from django.contrib import messages

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
                login(request, user)
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

def search(request):
    return render(request, 'dangun_app/trade.html')

def trade(request):
    top_views_posts = Post.objects.filter(product_sold='N').order_by('-views')
    return render(request, 'dangun_app/trade.html', {'posts': top_views_posts})

def trade_post(request, product_id):
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
        user_profile = UserProfile.objects.get(user=post.product_id)
    except UserProfile.DoesNotExist:
            user_profile = None

    context = {
        'post': post,
        'user_profile': user_profile,
        # 'chat_room': chat_room,
    }

    return render(request, 'dangun_app/trade_post.html', context)

@login_required
def write(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        image_form = PostImage(request.FILES.getlist("image"))
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = request.user
            post.save()
    
            for image in request.FILES.getlist("image"):
                image_form = PostImage(post_id=post.pk, image=image)
                image_form.save()

            return redirect('dangun_app:trade_post', product_id=post.pk)
    else:
        form = PostForm()
    return render(request,'dangun_app/write.html' , {'form': form})

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


# 채팅하기
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

from django.http import JsonResponse
from django.db.models import Q

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

@login_required
def chat_view(request):
    return render(request, 'dangun_app/chat.html')

@login_required
def get_latest_chat_no_pk(request):
    user = request.user
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user),
            latest_message_time__isnull=False
        ).latest('latest_message_time')
        return redirect('dangun_app:chat_room', pk=latest_chat.room_number)

    except ChatRoom.DoesNotExist:
        return redirect('dangun_app:alert', alert_message='진행중인 채팅이 없습니다.', redirect_url='current')
    
@method_decorator(login_required, name='dispatch')
class ConfirmDealView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        previous_url = request.META.get('HTTP_REFERER')
        url_parts = previous_url.split('/')
        original_post_id = url_parts[-2] if url_parts[-1] == '' else url_parts[-1]

        chat_room = get_object_or_404(ChatRoom, room_number=original_post_id)


        if chat_room.starter == user:
            other_user = chat_room.receiver
        else:
            other_user = chat_room.starter

        if chat_room is None:
            messages.error(request, 'Chat room does not exist.')
            return redirect('dangun_app:trade')
        
        # buyer를 설정하고, product_sold를 Y로 설정
        post.buyer = chat_room.receiver if chat_room.starter == post.user else chat_room.starter
        post.product_sold = 'Y'
        post.save()
        
        # 거래가 확정되면 새로고침
        return redirect('dangun_app:chat_room', pk=chat_room.room_number)
    
@login_required
def get_latest_chat(request, pk):
    user = request.user
    # 1) 해당 pk인 채팅방 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat_with_pk = ChatRoom.objects.filter(
            Q(post_id=pk) &
            (Q(receiver=user) | Q(starter=user))
        ).latest('latest_message_time')
        return JsonResponse({'success': True, 'chat_room_id': latest_chat_with_pk.room_number})
    except ChatRoom.DoesNotExist:
        pass

    # 2) 위 경우가 없다면 내가 소속된 채팅방 전체 중 가장 최신 채팅방으로 리디렉션
    try:
        latest_chat = ChatRoom.objects.filter(
            Q(receiver=user) | Q(starter=user)
        ).latest('latest_message_time')
        return JsonResponse({'success': True, 'chat_room_id': latest_chat.room_number})

    # 3) 모두 없다면 현재 페이지로 리디렉션
    except ChatRoom.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'alert_message': '진행중인 채팅이 없습니다.'
        })