"""
URL configuration for crs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('main.urls', namespace='main')),
    path('events/', include('events.urls', namespace='events')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('organizations/', include('organizations.urls', namespace='organizations')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('archive/', include('archive.urls', namespace='archive')),
    path('settings/', include('settings.urls', namespace='settings')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
