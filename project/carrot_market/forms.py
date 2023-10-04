from django import forms
from .models import Post, UserProfile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title' , 'price', 'product_description', 'deal_location']
        exclude = ['created_at', 'views','product_img', 'chat_num', 'product_sold', 'product_reserved']
        # 아이디 생성 시 user_id 제거

class CustomLoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'class': 'login-input'}),
        label='아이디',
        label_suffix='', 
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요', 'class': 'login-input'}),
        label='비밀번호',
        label_suffix='', 
    )
    class Meta:
        model = UserProfile
        fields = ['username', 'password']
        exclude = ['region_certification']

class CustomUserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'class': 'login-input'}),
        label='아이디',
        label_suffix='', 
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요', 'class': 'login-input'}),
        label='비밀번호',
        label_suffix='', 
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 다시 입력해주세요', 'class': 'login-input'}),
        label='비밀번호 확인',
        label_suffix='', 
    )
    class Meta:
        model = UserProfile
        fields = ['username', 'password1', 'password2']
        exclude = ['region_certification']