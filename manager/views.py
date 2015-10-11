from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from teams.models import Team
from tournament.models import Tournament, Division, Group, Signup
from tournament.forms import TournamentForm
from .decorators import staff_member_required
import datetime

@staff_member_required
def TeamDelete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    return redirect(teamManager)

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
def group_team_dropper(request, pk, team_pk=None):
    group = get_object_or_404(Group, pk=pk)
    if team_pk:
        team = get_object_or_404(Team, pk=team_pk)
        group.teams.remove(team)
        signup = Signup.objects.filter(tournament=group.division.tournament).filter(team=team)[0]
        signup.is_completed = False
        signup.save()
    else:
        for team in group.teams.all():
            group.teams.remove(team)
            signup = Signup.objects.filter(tournament=group.division.tournament).filter(team=team)[0]
            signup.is_completed = False
            signup.save()
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
            pass
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
