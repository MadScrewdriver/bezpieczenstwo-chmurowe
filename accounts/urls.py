"""
Plik urls.py w aplikacji 'accounts' – definiuje ścieżki:
- Rejestracja
- Logowanie
"""

from django.urls import path

from .views import register_view, logout_view, activate_account, CustomDisableView, confirm_disable_2fa, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='two_factor:login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uid>/<token>/', activate_account, name='activate'),
    path('two_factor/disable/', CustomDisableView.as_view(), name='two_factor:disable'),
    path('two_factor/disable-2fa-confirm/<uid>/<token>/', confirm_disable_2fa, name='disable_confirm'),
]
