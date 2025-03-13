"""
Plik views.py – zawiera logikę biznesową aplikacji 'accounts'.
Tutaj obsługujemy rejestrację, logowanie, 2FA oraz prosty ekran powitalny.
"""
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, resolve_url, get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.functional import lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from django_otp import devices_for_user
from django_otp.decorators import otp_required
from two_factor.forms import DisableForm
from django.core.signing import Signer, BadSignature
from two_factor.views.core import login_not_required, LoginView

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

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

            return render(request, 'two_factor/profile/verification_email_sent.html', {'email': user.email})

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


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('two_factor:profile')  # Redirect to profile page if user is authenticated
        return super().dispatch(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
class CustomDisableView(FormView):
    """
    Custom view that requires email confirmation before disabling 2FA.
    """
    template_name = 'two_factor/profile/disable.html'
    success_url = lazy(resolve_url, str)(settings.LOGIN_REDIRECT_URL)
    form_class = DisableForm

    def dispatch(self, *args, **kwargs):
        fn = otp_required(super().dispatch, login_url=self.success_url, redirect_field_name=None)
        return fn(*args, **kwargs)

    def form_valid(self, form):
        user = self.request.user

        # Send confirmation email
        subject = "Potwierdzenie wyłączenia uwierzytelniania dwuskładnikowego"
        subject = "Aktywuj swoje konto"
        message = render_to_string('email/email_2fa.html',
                                   {'user': user, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token': default_token_generator.make_token(user),
                                    'BASE_URL': settings.BASE_URL, })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

        return render(self.request, 'two_factor/profile/disable_email_sent.html')


def confirm_disable_2fa(request, uid, token):
    """
    View that processes the email confirmation for disabling 2FA.
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
