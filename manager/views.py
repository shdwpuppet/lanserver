from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from matches.models import Match
from teams.models import Team
from matches.forms import MatchForm
from tournament.models import Tournament, Division, Group, Signup, Server
from tournament.forms import TournamentForm, ServerForm
from .decorators import staff_member_required
import datetime

@staff_member_required
def TeamDelete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    return redirect(teamManager)

@staff_member_required
def serverdelete(request, id):
    server = get_object_or_404(Server, pk=id)
    server.delete()
    return redirect(serverManager)

@staff_member_required
def TournamentDelete(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    tournament.delete()
    return redirect(tournamentManager)

@staff_member_required
def tournament_setstatus(request, pk, status):
    tournament = Tournament.objects.get(pk=pk)
    tournament.status = status
    tournament.save()
    return redirect(tournamentManager)

@staff_member_required
def match_setup_complete(request, id):
    match = get_object_or_404(Match, pk=id)
    match.is_setup = True
    match.save()
    return redirect(matchManager)

@staff_member_required
def group_team_dropper(request, pk, team_pk=None):
    group = get_object_or_404(Group, pk=pk)
    if team_pk:
        team = get_object_or_404(Team, pk=team_pk)
        group.teams.remove(team)
        signup = Signup.objects.filter(tournament=group.division.tournament).filter(team=team)[0]
        signup.is_completed = False
        signup.save()
        team.rank_set.filter(group=group).delete()
    else:
        for team in group.teams.all():
            group.teams.remove(team)
            signup = Signup.objects.filter(tournament=group.division.tournament).filter(team=team)[0]
            signup.is_completed = False
            signup.save()

            team.rank_set.filter(group=group).delete()
    return redirect(tournamentDivGroupManager, pk=group.division.tournament_id)

@staff_member_required
def start_round(request, division_pk, group_pk=None):
    if not group_pk:
        division = get_object_or_404(Division, pk=division_pk)
        for group in division.group_set.all():
            group.start_round()
            group.update_max_round()
    else:
        group = get_object_or_404(Group, pk=group_pk)
        print('start round for group:' + group.name)
        group.start_round()
        group.update_max_round()
    return redirect(tournamentDivGroupManager, pk=group.division.tournament_id)


@staff_member_required
def teamManager(request):
    teams = Team.objects.all()
    return render(request, 'manager/manage_teams.html', {'teams': teams})

@staff_member_required
def matchManager(request, id=None):
    if id:
        match = get_object_or_404(Match, pk=id)
    else:
        match = Match()
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect(matchManager)
    form = MatchForm(instance=match)
    orphan_matches = Match.objects.filter(group=None, division=None)
    setup_matches = Match.objects.filter(server=None).exclude(is_setup=True)
    tournaments = Tournament.objects.all()
    context = {
        'orphan_matches': orphan_matches,
        'setup_matches': setup_matches,
        'tournaments': tournaments,
        'form': form,

    }
    return render(request, 'manager/manage_matches.html', context)

@staff_member_required
def serverManager(request, id=None):
    if id:
        server = get_object_or_404(Server, pk=id)
    else:
        server = Server()
    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            return redirect(serverManager)
    form = ServerForm(instance=server)
    servers_in_use = Server.objects.filter(is_in_use=True)
    servers = Server.objects.all()
    context = {
        'in_use': servers_in_use,
        'servers': servers,
        'form': form,

    }
    return render(request, 'manager/manage_servers.html', context)

@staff_member_required
def tournamentManager(request, id=None):
    if id:
        tournament = get_object_or_404(Tournament, pk=id)
        date_start = datetime.datetime.strftime(tournament.date_start, '%Y-%m-%d %H:%M')
        date_end = datetime.datetime.strftime(tournament.date_end, '%Y-%m-%d %H:%M')
    else:
        tournament = Tournament()
        date_start = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
        date_end = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=7), '%Y-%m-%d %H:%M')

    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            dates = request.POST.get('datetime').split(' - ')
            tournament.date_start = dates[0]
            tournament.date_end = dates[1]
            tournament.slug = slugify(tournament.name)
            tournament.save()
            form.save()

            return redirect(tournamentManager)
    form = TournamentForm(instance=tournament)
    tournaments = Tournament.objects.all()
    context = {
            'tournaments': tournaments,
            'form': form,
            'date_start': date_start,
            'date_end': date_end,
    }
    return render(request, 'manager/manage_tournaments.html', context)

@staff_member_required
def add_team_to_div_group(request, team_pk, tournament_pk, division_pk, group_pk=None):
    division = Division.objects.get(pk=division_pk)
    team = Team.objects.get(pk=team_pk)
    if group_pk:
        group = Group.objects.get(pk=group_pk)
        division.assign_team_to_group(team, group=group)
    else:
        division.assign_team_to_group(team=team)
        print("group matched to none")
    tournament = Tournament.objects.get(pk=tournament_pk)
    for signup in tournament.signup_set.filter(team=team):
        signup.is_completed = True
        signup.save()
    return render(request, 'manager/manage_tournament_divs.html', {'tournament': tournament})


@staff_member_required
def tournamentDivGroupManager(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.method == 'POST':
        if 'add_div' in request.POST:
            tournament.add_division(dtype=1, name=request.POST.get('name'), num_finalists=2)
            return redirect(tournamentDivGroupManager, pk=tournament.pk)
        elif 'add_group' in request.POST:
            div = Division.objects.get(pk=request.POST.get('div_id'))
            div.create_group(name=request.POST.get('name'), inc_in_assignment=True)
            return redirect(tournamentDivGroupManager, pk=tournament.pk)
        elif 'edit_div' in request.POST:
            pass
        elif 'edit_group' in request.POST:
            pass
        elif 'add_team_group' in request.POST:
            group = Group.objects.get(pk=request.POST.get('group'))
            team = Team.objects.get(name=request.POST.get('team_added'))
            group.division.assign_team_to_group(team=team, group=group)
            group.update_max_round()
            signup = Signup.objects.filter(team=team, tournament=tournament)
            signup.delete()
        elif 'add_team_div' in request.POST:
            pass
        elif 'remove_team_group' in request.POST:
            group = Group.objects.get(pk=request.POST.get('group'))
            team = Team.objects.get(pk=request.POST.get('team'))
            group.division.remove_team_from_group(team=team, group=group)
    return render(request, 'manager/manage_tournament_divs.html', {'tournament': tournament})
