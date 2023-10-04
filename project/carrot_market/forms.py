from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title' , 'price', 'product_description', 'deal_location']
        exclude = ['created_at', 'views', 'user_id','product_img', 'chat_num', 'product_sold', 'product_reserved']
        # 아이디 생성 시 user_id 제거
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
