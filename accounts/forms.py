"""
Plik forms.py – zawiera formularze do rejestracji i logowania
dla lokalnych użytkowników.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password


class UserRegistrationForm(forms.ModelForm):
    """
    Formularz rejestracji nowego użytkownika.
    """
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            self.add_error('password2', "Hasła nie są identyczne.")
        return cleaned_data


class LocalUserLoginForm(AuthenticationForm):
    """
    Formularz logowania dla zwykłych, lokalnych użytkowników.
    """
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
