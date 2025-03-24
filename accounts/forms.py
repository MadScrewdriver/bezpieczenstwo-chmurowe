"""
.. module:: accounts.forms
   :platform: Unix, Windows
   :synopsis: Formularze do rejestracji i logowania użytkowników lokalnych.

Formularze obsługujące proces rejestracji oraz logowania użytkowników w aplikacji ``accounts``.
Zawiera:
- Formularz rejestracyjny z walidacją haseł
- Formularz logowania dla lokalnych użytkowników

Wykorzystuje wbudowane modele i klasy Django, takie jak ``User``, ``AuthenticationForm``
oraz ``validate_password``.

"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password


class UserRegistrationForm(forms.ModelForm):
    """
    Formularz rejestracji nowego użytkownika.

    Rozszerza klasę ``ModelForm`` opartą o model ``User`` i umożliwia
    wprowadzenie hasła oraz jego potwierdzenia. Zastosowano walidację
    siły hasła za pomocą `validate_password`.

    Pola formularza:
    - ``username`` – nazwa użytkownika (z modelu User)
    - ``email`` – adres email użytkownika (z modelu User)
    - ``password`` – hasło główne (pole typu ``PasswordInput``)
    - ``password2`` – powtórzenie hasła (pole typu ``PasswordInput``)

    Walidacja:
    - Sprawdza, czy oba hasła są zgodne
    - Weryfikuje siłę hasła za pomocą walidatora Django
    """

    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        """
        Sprawdza, czy hasło i jego powtórzenie są identyczne.
        W przeciwnym razie zgłasza błąd walidacji.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Hasła nie są identyczne.")
        return cleaned_data


class LocalUserLoginForm(AuthenticationForm):
    """
    Formularz logowania dla lokalnych użytkowników.

    Rozszerza wbudowany formularz ``AuthenticationForm``, dodając własne etykiety
    dla pól logowania.

    Pola formularza:
    - ``username`` – nazwa użytkownika
    - ``password`` – hasło użytkownika
    """

    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
