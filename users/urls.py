from django.urls import path
from .views import UserRegisterView, login_view

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
] 