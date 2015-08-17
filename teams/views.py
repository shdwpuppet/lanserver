from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Team, Player
from .forms import TeamForm
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
	team_list = Team.objects.order_by('name')
	template = loader.get_template('team_index.html')
	context = RequestContext(request, {
		'team_list' : team_list,
	})
	return HttpResponse(template.render(context))
	
def details(request, team_id):
	team = get_object_or_404(Team, pk=team_id)
	return render(request, 'team_details.html', {'team': team})
	
def manage(request, team_id):
	pass

@login_required(login_url="/login/steam/")
def add_team(request):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save()
			Player.objects.add_player(user=request.user, team=team, position=1)
			return redirect(details, team_id=team.pk)
	else:
		form = TeamForm()
	return render(request, 'team_add.html', {'form': form})

