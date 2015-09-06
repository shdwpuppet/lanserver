from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from teams.models import Team
from tournament.models import Tournament, Division, Group, Signup
from tournament.forms import TournamentForm
from django.contrib.admin.views.decorators import staff_member_required
import datetime


class TeamDelete(DeleteView):
    model = Team
    success_url = reverse_lazy('team_manager')
    template_name = 'manager/confirm_delete.html'


class TournamentDelete(DeleteView):
    model = Tournament
    success_url = reverse_lazy('tournament_manager')
    template_name = 'manager/confirm_delete.html'

@staff_member_required
def tournament_setstatus(request, pk, status):
    tournament = Tournament.objects.get(pk=pk)
    tournament.status = status
    tournament.save()
    return redirect(tournamentManager)


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
            form.save(commit=False)
            dates = request.POST.get('datetime').split(' - ')
            tournament.date_start = dates[0]
            tournament.date_end = dates[1]
            tournament.slug = slugify(tournament.name)
            tournament.save()
            return redirect(tournamentManager)
    else:
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
            signup = Signup.objects.filter(team=team, tournament=tournament)
            signup.delete()
        elif 'add_team_div' in request.POST:
            pass
        elif 'remove_team_group' in request.POST:
            group = Group.objects.get(pk=request.POST.get('group'))
            team = Team.objects.get(pk=request.POST.get('team'))
            group.division.remove_team_from_group(team=team, group=group)
    return render(request, 'manager/manage_tournament_divs.html', {'tournament': tournament})
