"""
.. module:: accounts.pipeline
   :platform: Unix, Windows
   :synopsis: Niestandardowe kroki (pipelines) dla logowania społecznościowego.

Moduł zawiera dodatkowe funkcje używane w procesie uwierzytelniania przez
Google OAuth i inne platformy społecznościowe.

Zawiera:
- filtr dostępu dla kont administracyjnych (tylko ``is_staff`` + ``is_superuser``)
- własną implementację pobierania identyfikatora użytkownika (UID)
"""

from django.shortcuts import redirect


def verify_staff_status(backend, user, response, *args, **kwargs):
    """
    Zezwala tylko użytkownikom z uprawnieniami administracyjnymi na logowanie przez Google OAuth.

    Sprawdza, czy użytkownik jest oznaczony jako ``is_staff`` i ``is_superuser``.
    W przeciwnym razie następuje przekierowanie na stronę profilu (lub logowania) bez dostępu.

    :param backend: Obiekt backendu autoryzacji (np. GoogleOAuth2)
    :param user: Obiekt użytkownika Django
    :param response: Surowa odpowiedź z serwera OAuth (zawiera dane o użytkowniku)
    :return: ``redirect()`` w przypadku braku uprawnień lub ``None``
    """
    if not (user and user.is_staff and user.is_superuser):
        return redirect('two_factor:profile')


def social_uid(backend, details, response, *args, **kwargs):
    """
    Zwraca niestandardowy identyfikator użytkownika w zależności od użytego providera.

    Obsługiwani providerzy:
    - Microsoft Graph: zwraca ``userPrincipalName``
    - Facebook: zwraca ``email``
    - Domyślnie: używa metody ``get_user_id`` z backendu

    :param backend: Obiekt backendu autoryzacji
    :param details: Dane podstawowe o użytkowniku
    :param response: Surowa odpowiedź od providera
    :return: Słownik z kluczem ``uid`` zawierającym identyfikator użytkownika jako string
    """
    if backend.name == 'microsoft-graph':
        return {"uid": str(response.get("userPrincipalName"))}

    elif backend.name == 'facebook':
        return {"uid": str(response.get("email"))}

    return {"uid": str(backend.get_user_id(details, response))}
