# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def registration_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('user_profile')
    else:
        user_form = RegistrationForm()
    return render(request, 'registration.html', {'form': user_form})


def login_view(request):
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')

        # Попробуем аутентифицировать пользователя по username
        user = authenticate(request, username=login_input, password=password)

        if user is None:
            # Если не получилось, попробуем по email
            try:
                username = User.objects.get(email=login_input).username
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('user_profile')  # Перенаправление на страницу профиля пользователя после успешного входа
        else:
            form = AuthenticationForm(request.POST)
            form.add_error(None, 'Invalid login credentials')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

