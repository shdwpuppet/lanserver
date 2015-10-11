from django.conf.urls import url

urlpatterns = [
    url(r'setup/(?P<match_pk>\d+)/$', 'matches.views.match_setup', name='match_setup'),
    url(r'setup/(?P<match_id>\d+)/veto/(?P<map_id>\d+)/$', 'matches.views.veto_map', name='veto_map'),


]