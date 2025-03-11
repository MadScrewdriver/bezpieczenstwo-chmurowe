from urllib.parse import urlunparse, urlparse

from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.forms import UserRegistrationForm
from bezpieczenstwo_chmurowe import settings


class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('two_factor:login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('two_factor:profile')
        self.user_home_url = reverse('home')
        self.admin_login_url = reverse('social:begin', args=['google-oauth2'])

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def test_register_view_success(self):
        """Test poprawnej rejestracji użytkownika"""

        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'testpassword123@#',
            'password2': 'testpassword123@#',
            'email': 'newuser@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_view_invalid(self):
        """Test rejestracji z błędnymi danymi"""

        response = self.client.post(self.register_url, {
            'username': '',
            'password': 'testpassword123',
            'password2': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_logout_view(self):
        """Test wylogowania użytkownika"""

        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

    def test_user_home_view_authenticated(self):
        """Test dostępu do strony użytkownika po zalogowaniu"""

        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.user_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_url)

    def test_user_home_view_unauthenticated(self):
        """Test dostępu do strony użytkownika bez zalogowania"""

        response = self.client.get(self.user_home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.user_home_url}')

    def test_register_view_password_validation(self):
        """Test walidacji hasła podczas rejestracji"""

        weak_passwords = [
            '123456',
            'password',
            'testuser123',
            '123456789',
        ]

        for weak_password in weak_passwords:
            with self.subTest(password=weak_password):
                response = self.client.post(self.register_url, {
                    'username': 'testuser2',
                    'password1': weak_password,
                    'password2': weak_password,
                    'email': 'testuser2@example.com',
                })
                self.assertEqual(response.status_code, 200)
                self.assertFalse(User.objects.filter(username='testuser2').exists())

    def test_google_admin_login_redirect_unauthenticated(self):
        """Test przekierowania do Google OAuth dla administratora bez zalogowania"""

        response = self.client.get(self.admin_login_url)
        redirect_url = urlparse(response.url)._replace(query='')
        target_url = urlparse('https://accounts.google.com/o/oauth2/auth')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(redirect_url.scheme, target_url.scheme)

    def test_register_view_email_send(self):
        """Test wysłania emaila aktywacyjnego po rejestracji"""

        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'newuser@example.com'
        })

        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_active)
        self.assertEqual(len(mail.outbox), 1)

        email = mail.outbox[0]
        self.assertEqual(email.subject, "Aktywuj swoje konto")
        self.assertIn('newuser@example.com', email.to)
        self.assertIn(settings.BASE_URL, email.body)
        self.assertIn(str(user.pk), email.body)
