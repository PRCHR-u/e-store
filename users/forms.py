from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    avatar = forms.ImageField(required=False, label='Аватар')
    phone_number = forms.CharField(required=False, label='Номер телефона')
    country = forms.CharField(required=False, label='Страна')

    class Meta:
        model = CustomUser
        fields = ('email', 'avatar', 'phone_number', 'country', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Электронная почта')

    class Meta:
        model = CustomUser
        fields = ('username', 'password') 