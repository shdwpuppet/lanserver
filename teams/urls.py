from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<team_id>[0-9]+)/$', views.details, name='team_detail'),
    url(r'^create/$', views.add_team, name='add_team'),
    url(r'^leave/$', views.leave_team, name='leave_team'),
]