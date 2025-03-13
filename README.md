# Bezpieczeństwo Chmurowe

**Bezpieczeństwo Chmurowe** to aplikacja Django zbudowana pod audyt bezpieczeństwa chmurowego. 
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

## Tworzenie admina
```bash
  python manage.py createsuperuser
```

## Stwórz plik `.env` w głównym katalogu projektu i uzupełnij go zmiennymi środowiskowymi
```bash
  cp .env.example .env
```

## Uruchomienie serwera (musi być localhost)
```bash
python manage.py runserver localhost:8000
```
Otwórz przeglądarkę i wejdź na `http://localhost:8000`.

## Generowanie dokumentacji (Sphinx)
```bash
cd docs
make html
```
Dokumentacja znajduje się w `docs/_build/html/index.html`.

## Licencja
Projekt dostępny na licencji **MIT**. Szczegóły w pliku `LICENSE`.

