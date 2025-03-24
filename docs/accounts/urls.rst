urls.py
===========================

.. automodule:: accounts.urls
   :members:
   :undoc-members:
   :show-inheritance:

Opis ścieżek
------------

- **/login/** → widok logowania (z 2FA)
- **/register/** → formularz rejestracyjny
- **/logout/** → wylogowanie użytkownika
- **/activate/<uid>/<token>/** → aktywacja konta przez e-mail
- **/two_factor/disable/** → wyłączenie 2FA (krok 1)
- **/two_factor/disable-2fa-confirm/<uid>/<token>/** → potwierdzenie wyłączenia 2FA (krok 2)
