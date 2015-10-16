from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import RegisterForm
from teams.models import Team
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json, urllib
from django.conf import settings
from matches.models import Match

@login_required(login_url='/login/steam/')
def register(request):
    user = None
    template_name = 'register.html'
    success_url = '/dashboard/'
    user = request.user
    ll = user.last_login
    dj = user.date_joined
    td = ll-dj
    
    if (td.seconds == 0):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user.username = form.cleaned_data.get('username')
                user.save()
                return HttpResponseRedirect(success_url)
        else:
            form = RegisterForm()
            return render(request, template_name, {'form': form,})    
    else:
        return HttpResponseRedirect(success_url)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def self_profile(request):
    user = request.user
    team = Team.objects.filter(players__username=user.username)[0]
    steam_uid = user.social_auth.get().uid
    user_avatar = get_avatar(user)

    return render(request, 'profile.html', {'team': team, 'steam_uid': steam_uid, 'user_avatar': user_avatar})

def profile(request):
    pass

def get_avatar(user):
            steam_id = user.social_auth.get().uid
            key = settings.SOCIAL_AUTH_STEAM_API_KEY
            obj = urllib.request.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(key, steam_id)).read().decode()
            json_obj = json.loads(obj)
            return json_obj['response']['players'][0]['avatarfull']

def index(request):
    context = {}
    active_matches = Match.objects.exclude(result__isnull=False)
    context.update({"active_matches": active_matches})
    return render(request, 'index.html', context)
