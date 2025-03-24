"""
.. module:: accounts.tests
   :platform: Unix, Windows
   :synopsis: Zestaw testów sprawdzających widoki i funkcjonalność aplikacji ``accounts``.

.. moduleauthor:: Twoje Imię <twojemail@example.com>

Moduł zawiera testy związane z procesem rejestracji, logowania, wylogowywania
oraz dostępem do poszczególnych widoków w aplikacji ``accounts``.
"""

from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

from bezpieczenstwo_chmurowe import settings


class AccountsViewsTest(TestCase):
    """
    Klasa testowa sprawdzająca poprawne działanie widoków w aplikacji ``accounts``.

    Używa wbudowanego klienta testowego Django do wykonywania żądań HTTP.
    Sprawdza między innymi proces rejestracji, logowania, wylogowywania
    oraz dostęp do stron wymagających uwierzytelnienia.

    :cvar client: Instancja ``django.test.Client`` używana do wykonywania żądań HTTP w trakcie testów
    :cvar register_url: Adres URL dla rejestracji użytkownika
    :cvar login_url: Adres URL dla logowania (w tym przypadku obsługiwany przez pakiet two_factor)
    :cvar logout_url: Adres URL dla wylogowania użytkownika
    :cvar profile_url: Adres URL do profilu użytkownika
    :cvar user_home_url: Adres URL do strony głównej użytkownika
    :cvar admin_login_url: Adres URL do logowania administratora przez Google OAuth2
    :cvar user: Użytkownik testowy utworzony na potrzeby testów
    """

    def setUp(self):
        """
        Przygotowanie wstępne przed każdym testem.

        Tworzy klienta testowego, podstawowe adresy URL oraz użytkownika testowego.
        """
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('two_factor:login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('two_factor:profile')
        self.user_home_url = reverse('home')
        self.admin_login_url = reverse('social:begin', args=['google-oauth2'])

        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_register_view_success(self):
        """
        Test poprawnej rejestracji użytkownika.

        Sprawdza, czy użytkownik z prawidłowymi danymi rejestracyjnymi zostaje
        zapisany w bazie danych oraz czy otrzymuje właściwy kod statusu (200).
        """
        response = self.client.post(
            self.register_url,
            {
                'username': 'newuser',
                'password': 'testpassword123@#',
                'password2': 'testpassword123@#',
                'email': 'newuser@example.com',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_invalid(self):
        """
        Test rejestracji z błędnymi danymi.

        Sprawdza, czy w przypadku niepoprawnego uzupełnienia formularza rejestracyjnego
        (np. brak nazwy użytkownika, różne hasła), użytkownik nie zostanie utworzony w bazie.
        """
        response = self.client.post(
            self.register_url,
            {
                'username': '',
                'password': 'testpassword123',
                'password2': 'wrongpassword',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_logout_view(self):
        """
        Test wylogowania użytkownika.

        Sprawdza, czy po wylogowaniu użytkownik zostaje przekierowany
        na stronę logowania (kod statusu 302).
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_user_home_view_authenticated(self):
        """
        Test dostępu do strony użytkownika po zalogowaniu.

        Sprawdza, czy zalogowany użytkownik zostanie przekierowany
        na stronę profilu (kod statusu 302).
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.user_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_user_home_view_unauthenticated(self):
        """
        Test dostępu do strony użytkownika bez zalogowania.

        Sprawdza, czy niezalogowany użytkownik zostanie przekierowany
        na stronę logowania i czy w parametrach przekierowania
        znajduje się właściwy adres docelowy (``next=...``).
        """
        response = self.client.get(self.user_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{self.login_url}?next={self.user_home_url}'
        )

    def test_register_view_password_validation(self):
        """
        Test walidacji hasła podczas rejestracji.

        Przykład weryfikujący odrzucenie zbyt słabych haseł:
        - krótkich
        - zbyt oczywistych, jak ``password``
        - używających nazwy użytkownika
        """
        weak_passwords = ['123456', 'password', 'testuser123', '123456789']

        for weak_password in weak_passwords:
            with self.subTest(password=weak_password):
                response = self.client.post(
                    self.register_url,
                    {
                        'username': 'testuser2',
                        'password1': weak_password,
                        'password2': weak_password,
                        'email': 'testuser2@example.com',
                    }
                )
                self.assertEqual(response.status_code, 200)
                self.assertFalse(User.objects.filter(username='testuser2').exists())

    def test_register_view_email_send(self):
        """
        Test wysłania emaila aktywacyjnego po rejestracji.

        Sprawdza:
          * czy użytkownik po rejestracji jest nieaktywny (`is_active=False`),
          * czy w skrzynce nadawczej pojawiła się wiadomość e-mail,
          * czy temat oraz treść wiadomości zawierają oczekiwane informacje,
            takie jak link aktywacyjny i identyfikator użytkownika.
        """
        response = self.client.post(
            self.register_url,
            {
                'username': 'newuser',
                'password': 'testpassword123',
                'password2': 'testpassword123',
                'email': 'newuser@example.com',
            }
        )

        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, "Aktywuj swoje konto")
        self.assertIn('newuser@example.com', email.to)
        self.assertIn(settings.BASE_URL, email.body)
        self.assertIn(str(user.pk), email.body)
