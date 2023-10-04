from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser


class Post(models.Model):
    product_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default='oreumi')
    title = models.CharField(max_length=50)
    price = models.IntegerField() 
    product_description = models.TextField()
    deal_location = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='product_img/', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)

    product_reserved = models.CharField(max_length=1, default='N')  # 예약 여부
    product_sold = models.CharField(max_length=1, default='N')  # 판매 여부

    chat_num = models.PositiveIntegerField(default=0)  # 채팅 수

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class UserProfile(models.Model): # 이름 충돌때문에 수정
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    region_certification = models.CharField(max_length=1, default='N')
    location = models.CharField(max_length=100, null=True)
    
# 이미지 파일 테스트중
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post')
    image = models.ImageField(upload_to='product_img/', null=True)
    def __str__(self):
        return self.image.url

class Chat(models.Model):
    user_id = models.CharField(max_length=50)
    product_id = models.IntegerField()
    chatting = models.TextField(null=True)
    chatting_num = models.AutoField(primary_key=True) # room_num

class Address(models.Model):
    street_address = models.CharField(max_length=100)  # 도로명 주소
    city = models.CharField(max_length=50)             # 도시 또는 구
    state = models.CharField(max_length=50)            # 주 또는 시/도
    postal_code = models.CharField(max_length=10)       # 우편번호 (선택적)
    country = models.CharField(max_length=50)           # 국가 (선택적)

    def str(self):
        return f"{self.street_address}, {self.city}, {self.state}"

class ChatRoom(models.Model):
    room_number = models.AutoField(primary_key=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    chat_created_at = models.DateTimeField(auto_now_add=True)
    latest_message_time = models.DateTimeField(null=True, blank=True)
    chat_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chat_rooms', null=True, blank=True)


    def str(self):
        return f'ChatRoom: {self.starter.username} and {self.receiver.username}'

class Message(models.Model):
    chatroom = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Message: {self.author.username} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']

    def save(self, args, **kwargs):
        super().save(args, **kwargs)
        self.chatroom.latest_message_time = self.timestamp
        self.chatroom.save()

