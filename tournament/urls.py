from django.conf.urls import url
from tournament import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='Tournament List'),
    url(r'^(?P<slug>[\w-]+)/$', views.details),
    # url(r'^(?P<team_id>[0-9])/$', views.details, name='detail'),
    # url(r'^(?P<team_id>[0-9]+)/manage/$', views.manage, name='manage'),
    # url(r'^add/$', views.add_team, name='add_team'),
]
