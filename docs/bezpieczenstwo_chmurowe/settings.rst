bezpieczenstwo_chmurowe/settings.py
================================

.. automodule:: bezpieczenstwo_chmurowe.settings
   :members:
   :undoc-members:
   :show-inheritance:

Opis ustawień
-------------

**Środowisko i bezpieczeństwo**
- ``SECRET_KEY`` – klucz aplikacji, ładowany z `.env`
- ``DEBUG`` – tryb debugowania (``True``/``False``)
- ``ALLOWED_HOSTS`` – lista dozwolonych hostów (oddzielone przecinkami)

**Aplikacje Django**
- ``INSTALLED_APPS`` – zawiera aplikację `accounts`, `two_factor`, `social_django` oraz wtyczki OTP

**Middleware**
- ``MIDDLEWARE`` – middleware Django + ``OTPMiddleware`` do obsługi 2FA

**Szablony**
- ``TEMPLATES['DIRS']`` – katalog z szablonami (np. `templates/`)
- ``context_processors`` – standardowy zestaw + request context

**Baza danych**
- ``DATABASES`` – SQLite (można łatwo podmienić na PostgreSQL)

**Walidacja haseł**
- Lista validatorów w ``AUTH_PASSWORD_VALIDATORS`` zgodnie z best practices Django

**Międzynarodowość**
- ``LANGUAGE_CODE = 'pl'``, ``TIME_ZONE = 'UTC'``, ``USE_TZ = True``

**Ścieżki plików statycznych**
- ``STATIC_URL``, ``MEDIA_URL``

**Uwierzytelnianie i logowanie**
- ``AUTHENTICATION_BACKENDS`` – obsługa Google, Microsoft, Facebook i Django
- ``LOGIN_URL``, ``LOGOUT_REDIRECT_URL`` – ścieżki po zalogowaniu/wylogowaniu

**Social Auth – konfiguracja**
- ``SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`` / ``SECRET``
- ``SOCIAL_AUTH_FACEBOOK_KEY`` / ``SECRET``
- ``SOCIAL_AUTH_MICROSOFT_GRAPH_KEY`` / ``SECRET``
- ``SOCIAL_AUTH_PIPELINE`` – niestandardowe kroki z aplikacji `accounts.pipeline`

**E-mail**
- ``EMAIL_BACKEND`` – SMTP (Gmail)
- ``EMAIL_HOST_USER`` – domyślny nadawca
- ``EMAIL_HOST_PASSWORD`` – hasło z `.env`
- ``DEFAULT_FROM_EMAIL`` – używane w `send_mail`

**Inne**
- ``BASE_URL`` – używane w wiadomościach e-mail (do generowania linków aktywacyjnych)

