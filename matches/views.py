from django.shortcuts import render, get_object_or_404, redirect
from matches.models import Match, Result, Map
from tournament.models import Server
import random


def detail(request, match_pk):
    match = get_object_or_404(Match, pk=match_pk)
    if request.method == "POST":
        pass
    else:
        pass

def veto_map(request, match_id, map_id):
    match = get_object_or_404(Match, pk=match_id)
    captains = match.home_team.get_captains() | match.away_team.get_captains()
    if request.user.player_set.all()[0] in captains or request.user.is_staff:
        map = get_object_or_404(Map, pk=map_id)
        if request.user.team_set.all()[0] == match.home_team:
            match.home_veto.add(map)
            match.veto_turn = 1
            match.save()
        else:
            match.away_veto.add(map)
            match.veto_turn = 0
            match.save()

        return redirect(match_setup, match_pk=match_id)
    else:
        return redirect(detail, match_pk=match_id)

def match_setup(request, match_pk):
    match = get_object_or_404(Match, pk=match_pk)
    captains = match.home_team.get_captains() | match.away_team.get_captains()
    if request.user.player_set.all()[0] in captains or request.user.is_staff:
        context={'match': match}
        map_pool = list(match.group.division.tournament.map_pool.all())
        [map_pool.remove(map) for map in map_pool if map in match.away_veto.all()]
        [map_pool.remove(map) for map in map_pool if map in match.home_veto.all()]
        context.update({'maps_remaining': map_pool})

        if len(match.home_veto.all()) == match.vetoes and len(match.away_veto.all()) == match.vetoes and not match.map:
            match.map = random.choice(map_pool)
            match.save()

        if not match.map:
            context.update({'phase': 'pick_map'})
            if match.veto_turn == 0:
                context.update({'picking_team': match.home_team})
            else:
                context.update({'picking_team': match.away_team})
        else:
            match.server = random.choice(Server.objects.filter(is_in_use=False))
            match.save()
            pass
        if request.method == 'POST':
            result = Result()
            result.match = match
            result.record_result(t1=match.home_team, s1=request.POST.get('home_score'), t2=match.away_team, s2=request.POST.get('away_score'))
            result.save()
            return redirect(detail, match_pk=match_pk)
        return render(request, 'match_setup.html', context)
    else:
        return redirect(detail, match_pk=match_pk)
