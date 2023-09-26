from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['created_at', 'views', 'user_id']
        # 아이디 생성 시 user_id 제거

