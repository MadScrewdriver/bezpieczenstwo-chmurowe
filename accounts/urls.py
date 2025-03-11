"""
Plik urls.py w aplikacji 'accounts' – definiuje ścieżki:
- Rejestracja
- Logowanie
"""

from django.urls import path
from .views import register_view, logout_view, activate_account

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('activate/<uid>/<token>/', activate_account, name='activate'),
]
