"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
import os
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from ecommerce.views import about_page, contact_page, home_page

urlpatterns = [
    path('', home_page, name='home'),
    path('about', about_page, name='about'),
    path('contact', contact_page, name='contact'),
    path('products/', include("products.urls", namespace='products')),
    path('cart/', include("cart.urls", namespace='cart')),
    path('tinymce/', include('tinymce.urls')),

    path('', include("users.urls", namespace='users')),

    path('admin/', admin.site.urls), # admin site
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
