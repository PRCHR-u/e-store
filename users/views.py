from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm
from .models import CustomUser

# Create your views here.

class UserRegisterView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.avatar = form.cleaned_data.get('avatar')
        user.phone_number = form.cleaned_data.get('phone_number')
        user.country = form.cleaned_data.get('country')
        user.save()
        login(self.request, user)
        send_mail(
            'Добро пожаловать!',
            'Спасибо за регистрацию в нашем сервисе!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        messages.success(self.request, 'Регистрация прошла успешно!')
        return super().form_valid(form)

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Неверная электронная почта или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
