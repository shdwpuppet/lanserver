from django.conf.urls import include, url
from django.views.generic import TemplateView
from core.views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', 'core.views.index', name="index"),
    url(r'^teams/', include('teams.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^tournaments/', include('tournament.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^register/', register, name='register'),
    url(r'^logout/', 'core.views.logout_view', name='logout'),
    url(r'^profile/', 'core.views.self_profile', name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', 'core.views.profile', name='other profile'),
    url(r'^match/', include('matches.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)