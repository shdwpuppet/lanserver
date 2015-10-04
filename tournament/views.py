from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from tournament.models import Tournament, Division


class index(ListView):
    model = Tournament
    template_name = "tournament_list.html"


def details(request, slug):
    context = dict()
    tournament = get_object_or_404(Tournament, slug=slug)
    context.update({'tournament': tournament})
    signups = [signup.team for signup in tournament.signup_set.all()]
    user_teams = request.user.team_set.all()
    context.update({'eligible': not [i for i in signups if i in user_teams]})
    if request.method == "POST":
        if 'signup' in request.POST and [request.user in user_teams[0].get_captains()]:
            div = get_object_or_404(Division, name=request.POST['signup'], tournament=tournament)
            tournament.signup(team=user_teams[0], requested_div=div)
            context.update({'eligible': False})
    return render(request, 'tournament_details.html', context)
