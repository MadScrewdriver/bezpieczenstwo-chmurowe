urls.py
===========

.. automodule:: bezpieczenstwo_chmurowe.urls
   :members:
   :undoc-members:
   :show-inheritance:

Opis ścieżek
------------

- **/** → strona domowa po zalogowaniu użytkownika (przekierowuje do profilu)
- **/admin/login/** → przekierowanie logowania admina do logowania z 2FA
- **/admin/** → panel administracyjny Django
- **/oauth/** → logowanie społecznościowe (Google, Microsoft, Facebook itp.)
- **/account/** → podłączenie ścieżek z aplikacji „accounts”
- **ścieżki z django-two-factor-auth** → logowanie z 2FA, konfiguracja urządzeń itp.
- **catch-all (`^.*$`)** → dowolna inna ścieżka przekierowuje na stronę domową użytkownika
