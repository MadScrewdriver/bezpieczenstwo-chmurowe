"""
.. module:: accounts.views
   :platform: Unix, Windows
   :synopsis: Widoki logiki użytkownika w aplikacji ``accounts``.

Plik zawiera widoki obsługujące:
- rejestrację użytkownika z e-mailową aktywacją konta,
- logowanie i wylogowanie (w tym z 2FA),
- ekran powitalny użytkownika,
- proces wyłączania dwuetapowej weryfikacji (2FA) z potwierdzeniem e-mailowym.
"""

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, resolve_url, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.functional import lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import FormView
from django_otp import devices_for_user
from django_otp.decorators import otp_required
from two_factor.forms import DisableForm
from two_factor.views.core import login_not_required, LoginView

from accounts.forms import UserRegistrationForm


def register_view(request):
    """
    Widok rejestracji nowego użytkownika z e-mailowym potwierdzeniem.

    Jeśli formularz rejestracyjny jest poprawny:
    - Tworzy użytkownika w stanie nieaktywnym.
    - Wysyła e-mail aktywacyjny z linkiem zawierającym UID i token.
    - Wyświetla stronę potwierdzenia wysłania wiadomości.

    :param request: Obiekt żądania HTTP
    :return: Strona z formularzem lub komunikatem o wysłaniu maila
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            subject = "Aktywuj swoje konto"
            message = render_to_string('email/email_verification.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'BASE_URL': settings.BASE_URL,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

            return render(request, 'two_factor/profile/verification_email_sent.html', {'email': user.email})
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account(request, uid, token):
    """
    Aktywuje konto użytkownika po kliknięciu w link z wiadomości e-mail.

    Jeśli UID i token są poprawne:
    - Aktywuje konto (ustawia ``is_active=True``).
    - Przekierowuje na stronę profilu.

    :param request: Obiekt żądania HTTP
    :param uid: Zakodowany identyfikator użytkownika
    :param token: Token aktywacyjny
    :return: Przekierowanie na stronę profilu
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
    Wylogowuje użytkownika i przekierowuje na stronę logowania.

    :param request: Obiekt żądania HTTP
    :return: Przekierowanie na login
    """
    logout(request)
    return redirect('two_factor:login')


@login_required
def user_home_view(request):
    """
    Widok dostępny tylko dla zalogowanych użytkowników.

    Przekierowuje do profilu użytkownika po zalogowaniu.

    :param request: Obiekt żądania HTTP
    :return: Przekierowanie na stronę profilu
    """
    return redirect('two_factor:profile')


class CustomLoginView(LoginView):
    """
    Niestandardowy widok logowania.

    Jeśli użytkownik jest już zalogowany, przekierowuje go na stronę profilu.
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('two_factor:profile')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
class CustomDisableView(FormView):
    """
    Widok formularza do wyłączenia 2FA z e-mailowym potwierdzeniem.

    - Użytkownik wypełnia formularz wyłączenia.
    - Na e-mail wysyłany jest link potwierdzający.
    """
    template_name = 'two_factor/profile/disable.html'
    success_url = lazy(resolve_url, str)(settings.LOGIN_REDIRECT_URL)
    form_class = DisableForm

    def dispatch(self, *args, **kwargs):
        fn = otp_required(super().dispatch, login_url=self.success_url, redirect_field_name=None)
        return fn(*args, **kwargs)

    def form_valid(self, form):
        """
        Wysłanie wiadomości e-mail z linkiem potwierdzającym wyłączenie 2FA.

        :param form: Wypełniony formularz DisableForm
        :return: Strona z komunikatem o wysłaniu wiadomości
        """
        user = self.request.user

        subject = "Aktywuj swoje konto"
        message = render_to_string('email/email_2fa.html', {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'BASE_URL': settings.BASE_URL,
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

        return render(self.request, 'two_factor/profile/disable_email_sent.html')


def confirm_disable_2fa(request, uid, token):
    """
    Potwierdzenie dezaktywacji 2FA przez kliknięcie w link z e-maila.

    Jeśli token jest poprawny:
    - Usuwa urządzenia OTP przypisane do użytkownika.

    :param request: Obiekt żądania HTTP
    :param uid: Zakodowany identyfikator użytkownika
    :param token: Token potwierdzający
    :return: Przekierowanie na stronę profilu
    """
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        for device in devices_for_user(request.user):
            device.delete()

    return redirect('two_factor:profile')
