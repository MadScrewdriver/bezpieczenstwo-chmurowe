# Bezpieczeństwo Chmurowe

**Bezpieczeństwo Chmurowe** to aplikacja Django zapewniająca bezpieczne uwierzytelnianie użytkowników, w tym logowanie do panelu administracyjnego wyłącznie przez Google OAuth. Lokalni użytkownicy mogą się rejestrować i logować przez formularz z obsługą dwuskładnikowego uwierzytelniania (2FA).

## Spis treści
- [Funkcjonalności](#funkcjonalności)
- [Wymagania](#wymagania)
- [Instalacja](#instalacja)
- [Testy](#testy)
- [Tworzenie superużytkownika](#tworzenie-superużytkownika)
- [Zmienne środowiskowe (`.env`) do uzupelnienia](#zmienne-środowiskowe-env-do-uzupelnienia)
- [Uruchomienie](#uruchomienie)
- [Generowanie dokumentacji (Sphinx)](#generowanie-dokumentacji-sphinx)
- [Licencja](#licencja)

## Funkcjonalności
- **Logowanie do panelu administracyjnego** wyłącznie przez Google OAuth.
- **Rejestracja** i **logowanie lokalne** użytkowników.
- **2FA (dwuskładnikowe uwierzytelnianie)** dla kont lokalnych.

## Wymagania
- Python 3.13+


## Instalacja
```bash
git clone https://github.com/MadScrewdriver/bezpieczenstwo-chmurowe.git
cd bezpieczenstwo-chmurowe
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Testy
```bash
  python manage.py test
```

## Tworzenie superużytkownika
```bash
  python manage.py createsuperuser
```

## Zmienne środowiskowe (`.env`) do uzupelnienia
```bash
SECRET_KEY= # klucz tajny Django
DEBUG= # True/False
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY= # klucz OAuth Google
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET= # sekret OAuth Google
```

## Uruchomienie
```bash
python manage.py runserver
```
Otwórz przeglądarkę i wejdź na `http://127.0.0.1:8000/`.

## Generowanie dokumentacji (Sphinx)
```bash
cd docs
make html
```
Dokumentacja znajduje się w `docs/_build/html/index.html`.

## Licencja
Projekt dostępny na licencji **MIT**. Szczegóły w pliku `LICENSE`.

