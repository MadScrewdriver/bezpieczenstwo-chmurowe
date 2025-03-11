"""
ASGI config for bezpieczenstwo_chmurowe project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bezpieczenstwo_chmurowe.settings')

application = get_asgi_application()
