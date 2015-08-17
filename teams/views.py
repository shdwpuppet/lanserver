from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Team
# Create your views here.

def index(request):
    item_list = Team.objects.order_by('name')
    output = ', '.join([t.name for t in item_list])
    return HttpResponse(output)
    
def details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    return render(request, 'team_details.html', {'team': team})
    
def manage(request, team_id):
    pass