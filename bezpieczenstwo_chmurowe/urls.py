"""
Plik urls.py – główna mapa URL dla aplikacji 'bezpieczenstwo_chmurowe'.
Zawiera przekierowania do panelu administracyjnego (tylko przez social-auth),
ścieżki do aplikacji 'accounts' itp.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from two_factor.urls import urlpatterns as tf_urls

from accounts.views import user_home_view


def redirect_to_admin(request):
    if request.user.is_authenticated:
        if request.user.is_staff and request.user.is_superuser:
            return redirect('admin')
        else:
            return redirect('home')
    return redirect('social:begin', backend='google-oauth2')


urlpatterns = [
    path('', user_home_view, name='home'),
    path('admin/login/', redirect_to_admin, name='admin_redirect'),
    path('admin/', admin.site.urls, name='admin'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('account/', include('accounts.urls')),
    path('', include(tf_urls)),
    re_path(r'^.*$', user_home_view, name='catch_all'),
]
