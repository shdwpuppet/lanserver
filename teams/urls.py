from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<team_id>[0-9])/$', views.details, name='detail'),
    url(r'^(?P<team_id>[0-9]+)/manage/$', views.manage, name='manage'),
]