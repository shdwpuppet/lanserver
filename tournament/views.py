from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context, loader
from django.views.generic import ListView
from tournament.models import Tournament, Division

# Create your views here.

class index(ListView):
    model = Tournament
    template_name = "tournament_list.html"

def details(request, slug):
    tournament = get_object_or_404(Tournament, slug=slug)
    
    template = loader.get_template("tournament_details.html")
    return render(request, 'tournament_details.html', {'tournament': tournament})