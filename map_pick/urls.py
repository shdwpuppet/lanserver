from django.conf.urls import url
from map_pick import views

urlpatterns = [
    url(r'^$', views.MapPickCreate.as_view(), name='map_pick_index'),
    url(r'^(?P<pk>[0-9]+)/$', views.mappick, name='map_pick'),
]
