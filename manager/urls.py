from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    url(r'^manage_teams/delete/(?P<pk>\d+)/$', staff_member_required(views.TeamDelete.as_view()), name="delete_team"),
    url(r'^manage_teams/$', 'manager.views.teamManager', name='team_manager'),
    url(r'^manage_tournaments/(?P<pk>\d+)/status/(?P<status>[1-4]+)/$', 'manager.views.tournament_setstatus', name='set_status'),
    url(r'^manage_tournaments/delete/(?P<pk>\d+)/$', staff_member_required(views.TournamentDelete.as_view()), name='delete_tournament'),
    url(r'^manage_tournaments/$', 'manager.views.tournamentManager', name='tournament_manager'),
    url(r'^manage_tournaments/edit/(?P<id>\d+)/$', 'manager.views.tournamentManager', name='edit_tournament'),
    url(r'^manage_tournaments/divs/(?P<pk>\d+)/$', 'manager.views.tournamentDivGroupManager', name='divgroup_tournament'),

]   