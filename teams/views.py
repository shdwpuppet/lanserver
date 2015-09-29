from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Team, Player
from .forms import TeamForm
from django.db.models import Count
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def index(request):
    team_list = Team.objects.order_by('name').annotate(
        player_count=Count('players'))
    template = loader.get_template('team_index.html')
    context = RequestContext(request, {
        'team_list': team_list,
    })
    return HttpResponse(template.render(context))


def details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    context = {'team': team}
    if request.user.is_authenticated() and request.user.player_set.get() in team.get_captains():
        context.update({'is_captain': True})
        if request.method == 'POST':
            if 'save_changes' in request.POST:
                form = TeamForm(request.POST, instance=team)
                if form.is_valid():
                    form.save()
                    return redirect('teams.views.details', team_id=team_id)
            elif 'change_captain' in request.POST:
                team.change_captain(Player.objects.get(name=request.POST.get('new_captain')))
                return redirect('teams.views.details', team_id=team_id)
        else:
            context.update({'form': TeamForm(instance=team)})
    return render(request, 'team_details.html', context)



@login_required(login_url="/login/steam/")
def add_team(request):
    if Team.objects.filter(players=request.user):
        messages.error(request, 'You are already on a team. Please leave your current team in order to form a new team.')
        form = TeamForm()
    else:
        if request.method == 'POST':
            form = TeamForm(request.POST)
            if form.is_valid():
                team = form.save()
                Player.objects.add_player(user=request.user, team=team, position=1)
                return redirect('team_details.html', {'team': team})
        else:
            form = TeamForm()
    return render(request, 'team_add.html', {'form': form})
