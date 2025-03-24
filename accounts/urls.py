"""
.. module:: accounts.urls
   :platform: Unix, Windows
   :synopsis: Ścieżki URL aplikacji ``accounts``.

Plik definiuje ścieżki URL obsługujące logowanie, rejestrację i
zarządzanie dwuetapową weryfikacją (2FA) w aplikacji użytkownika.

Dostępne ścieżki:
- Logowanie (z 2FA)
- Rejestracja nowego użytkownika
- Wylogowanie
- Aktywacja konta przez e-mail
- Dezaktywacja uwierzytelnienia dwuskładnikowego
"""

from django.urls import path

from .views import (
    register_view,
    logout_view,
    activate_account,
    CustomDisableView,
    confirm_disable_2fa,
    CustomLoginView
)

#: Lista ścieżek URL obsługiwanych przez aplikację ``accounts``
urlpatterns = [
    # Widok logowania z obsługą dwuetapowej weryfikacji
    path('login/', CustomLoginView.as_view(), name='two_factor:login'),

    # Rejestracja nowego użytkownika
    path('register/', register_view, name='register'),

    # Wylogowanie użytkownika
    path('logout/', logout_view, name='logout'),

    # Aktywacja konta przez link e-mailowy
    path('activate/<uid>/<token>/', activate_account, name='activate'),

    # Wyłączenie uwierzytelniania dwuskładnikowego – krok 1
    path('two_factor/disable/', CustomDisableView.as_view(), name='two_factor:disable'),

    # Potwierdzenie dezaktywacji 2FA – krok 2
    path('two_factor/disable-2fa-confirm/<uid>/<token>/', confirm_disable_2fa, name='disable_confirm'),
]
