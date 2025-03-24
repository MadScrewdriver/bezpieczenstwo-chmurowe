"""
.. module:: bezpieczenstwo_chmurowe.urls
   :platform: Unix, Windows
   :synopsis: Główna mapa URL aplikacji ``bezpieczenstwo_chmurowe``.

Plik odpowiada za główną konfigurację URL projektu Django.

Zawiera:
- przekierowanie do logowania admina przez 2FA,
- podłączenie ścieżek z aplikacji ``accounts``,
- integrację z ``django-two-factor-auth`` oraz ``social-auth-app-django``,
- ścieżkę domyślną i rezerwową (catch-all).
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from two_factor.urls import urlpatterns as tf_urls

from accounts.views import user_home_view


def redirect_admin(request):
    """
    Przekierowuje próbę logowania do panelu admina na stronę logowania z 2FA.

    :param request: Obiekt żądania HTTP
    :return: Przekierowanie do widoku logowania (two_factor:login)
    """
    return redirect('two_factor:login')


#: Lista głównych ścieżek URL projektu Django
urlpatterns = [
    # Strona główna (wymaga zalogowania) – np. po aktywacji konta
    path('', user_home_view, name='home'),

    # Przekierowanie logowania admina do logowania 2FA
    path('admin/login/', redirect_admin, name='admin_redirect'),

    # Panel administracyjny Django
    path('admin/', admin.site.urls, name='admin'),

    # Ścieżki autoryzacji społecznościowej (Google, Microsoft itd.)
    path('oauth/', include('social_django.urls', namespace='social')),

    # Ścieżki aplikacji accounts
    path('account/', include('accounts.urls')),

    # Ścieżki 2FA (django-two-factor-auth)
    path('', include(tf_urls)),

    # Catch-all – każde inne żądanie przekierowywane na stronę domową
    re_path(r'^.*$', user_home_view, name='catch_all'),
]
