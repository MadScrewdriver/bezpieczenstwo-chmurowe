"""
Plik views.py – zawiera logikę biznesową aplikacji 'accounts'.
Tutaj obsługujemy rejestrację, logowanie, 2FA oraz prosty ekran powitalny.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required

from .forms import UserRegistrationForm, LocalUserLoginForm
from django.contrib.auth.models import User


def register_view(request):
    """
    Rejestracja nowego użytkownika (lokalnego) z podstawową walidacją.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('two_factor:profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    """
    Wylogowanie użytkownika i przekierowanie na stronę główną.
    """
    logout(request)
    return redirect('two_factor:login')


@login_required
def user_home_view(request):
    """
    Ekran dostępny tylko dla zalogowanych (i potwierdzonych 2FA) użytkowników.
    Wyświetla prosty napis powitalny.
    """
    return redirect('two_factor:profile')
