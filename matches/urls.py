from django.conf.urls import url

urlpatterns = [
    url(r'/(?P<match_pk>\d+)/$', 'matches.views.detail', name='match_detail'),
]