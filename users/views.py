# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm


def registration_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_profile')  # Перенаправьте на страницу успешной регистрации
    else:
        user_form = RegistrationForm()
    return render(request, 'registration.html', {'form': user_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_profile')  # Перенаправление на страницу профиля пользователя после успешного входа
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

