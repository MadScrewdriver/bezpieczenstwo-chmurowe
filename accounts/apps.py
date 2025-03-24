"""
.. module:: accounts.apps
   :platform: Unix, Windows
   :synopsis: Konfiguracja aplikacji accounts.

Moduł zawiera konfigurację aplikacji ``accounts``,
zgodną z systemem aplikacji Django.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Konfiguracja aplikacji Django ``accounts``.

    Określa nazwę aplikacji i domyślny typ klucza głównego dla modeli.

    Atrybuty:
        default_auto_field (str): Domyślny typ pola dla automatycznego klucza głównego.
        name (str): Nazwa aplikacji Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
