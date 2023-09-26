from django.utils import timezone
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    location = models.CharField(max_length=100, null=True)

class Post(models.Model):
    product_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, default='oreumi')
    title = models.CharField(max_length=50)
    price = models.IntegerField() 
    product_description = models.TextField()
    deal_location = models.CharField(max_length=100)
    product_img = models.ImageField(upload_to='product_img/')
    created_at = models.DateTimeField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)

class Chat(models.Model):
    user_id = models.CharField(max_length=50)
    product_id = models.IntegerField()
    chatting = models.TextField(null=True)
    chatting_num = models.AutoField(primary_key=True)

