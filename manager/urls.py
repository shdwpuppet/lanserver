from django.conf.urls import url
from .decorators import staff_member_required

from . import views

urlpatterns = [
    url(r'^manage_teams/delete/(?P<pk>\d+)/$', staff_member_required(views.TeamDelete), name="delete_team"),
    url(r'^manage_teams/$', 'manager.views.teamManager', name='team_manager'),
    url(r'^manage_tournaments/(?P<pk>\d+)/status/(?P<status>[1-4]+)/$', 'manager.views.tournament_setstatus', name='set_status'),
    url(r'^manage_tournaments/delete/(?P<pk>\d+)/$', staff_member_required(views.TournamentDelete, login_url="social:login"), name='delete_tournament'),
    url(r'^manage_tournaments/$', 'manager.views.tournamentManager', name='tournament_manager'),
    url(r'^manage_tournaments/edit/(?P<id>\d+)/$', 'manager.views.tournamentManager', name='edit_tournament'),
    url(r'^manage_tournaments/divs/(?P<pk>\d+)/$', 'manager.views.tournamentDivGroupManager', name='divgroup_tournament'),
    url(r'^assign_group/(?P<team_pk>\d+)/(?P<tournament_pk>\d+)/(?P<division_pk>\d+)/(?P<group_pk>\d+)/$', 'manager.views.add_team_to_div_group', name="add_team_to_group"),
    url(r'^assign_group/(?P<team_pk>\d+)/(?P<tournament_pk>\d+)/(?P<division_pk>\d+)/$', 'manager.views.add_team_to_div_group', name="add_team_to_div"),

]
