"""lanserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from core.views import register, logout
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^teams/', include('teams.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^tournaments/', include('tournament.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register/', register, name='register'),
    url(r'^logout/', 'core.views.logout_view', name='logout'),
    url(r'^profile/', 'core.views.self_profile', name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', 'core.views.profile', name='other profile'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)