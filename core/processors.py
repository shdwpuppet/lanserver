import urllib
import json
from django.conf import settings
from teams.models import Team
from tournament.models import Tournament


def avatar(request):
    if hasattr(request, 'user'):
        if request.user.is_authenticated():
            user = request.user
            steam_id = user.social_auth.get().uid
            key = settings.SOCIAL_AUTH_STEAM_API_KEY
            obj = urllib.request.urlopen("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}".format(key, steam_id)).read().decode()
            json_obj = json.loads(obj)
            return {
                'avatar':   json_obj['response']['players'][0]['avatarfull'],
            }
        return {}
    return {}


def user_team(request):
    context = {}
    if hasattr(request, 'user'):
        if request.user.is_authenticated():
            user = request.user
            teams = Team.objects.filter(players=user)
            if teams:
                context['user_team'] = teams[0]
                if [player.user for player in teams[0].get_captains()] == [user]:
                    context['user_team_captain'] = True
    return context


def tournaments(request):
    tournaments = Tournament.objects.get(is_active=True)
