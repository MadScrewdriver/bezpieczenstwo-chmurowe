"""
Plik views.py – zawiera logikę biznesową aplikacji 'accounts'.
Tutaj obsługujemy rejestrację, logowanie, 2FA oraz prosty ekran powitalny.
"""
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.forms import UserRegistrationForm


def register_view(request):
    """
    Rejestracja nowego użytkownika z potwierdzeniem e-mail.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            subject = "Aktywuj swoje konto"
            message = render_to_string('email/email_verification.html',
                                       {'user': user, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': default_token_generator.make_token(user),
                                        'BASE_URL': settings.BASE_URL, })

            send_mail(subject, message, 'bezpieczenstwochmurowe@gmail.com', [user.email], fail_silently=False)

            return redirect('two_factor:login')

    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account(request, uid, token):
    """
    Aktywuje konto użytkownika po kliknięciu w link e-mailowy.
    """
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

    return redirect('two_factor:profile')


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
