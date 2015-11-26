from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from .forms import MapPickForm
from .models import MapPick
from django.http import JsonResponse


def api(request, pk):
    map_pick = get_object_or_404(MapPick, pk=pk)

    blue_picks = []
    blue_bans = []
    red_picks = []
    red_bans = []
    default_picks = []
    default_bans = []

    for map in map_pick.map_pool.all():
        if map_pick.map_banned(map.pk):
            if map_pick.map_banned_by(map.pk) == map_pick.team1:
                blue_bans.append(map.name)
            elif map_pick.map_banned_by(map.pk) == map_pick.team2:
                red_bans.append(map.name)
            else:
                default_bans.append(map.name)
        elif map_pick.map_picked(map.pk):
            if map_pick.map_picked_by(map.pk) == map_pick.team1:
                blue_picks.append(map.name)
            elif map_pick.map_picked_by(map.pk) == map_pick.team2:
                red_picks.append(map.name)
            else:
                default_picks.append(map.name)

    to_json = {
        'blue_picks': blue_picks,
        'blue_bans': blue_bans,
        'red_picks': red_picks,
        'red_bans': red_bans,
        'default_picks': default_picks,
        'default_bans': default_bans,
    }
    return JsonResponse(to_json, safe=False)


class MapPickCreate(CreateView):
    form_class = MapPickForm
    template_name = 'map_pick_index.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('map_pick', kwargs={'pk': pk})


def mappick(request, pk):
    map_pick = get_object_or_404(MapPick, pk=pk)
    maps = list()
    current = map_pick.current()

    if map_pick.current()[0] == 'default':
        map_pick.last_pick()


    for map in map_pick.map_pool.all():
        if map_pick.map_banned(map.pk):
            info = {
                'map': map.name,
                'status': 2,
                'by': map_pick.map_banned_by(map.pk),
            }
            maps.append(info)
        elif map_pick.map_picked(map.pk):
            info = {
                'map': map.name,
                'status': 1,
                'by': map_pick.map_picked_by(map.pk),
            }
            maps.append(info)
        else:
            info = {
                'pk': map.pk,
                'map': map.name,
                'status': 0,
            }
            maps.append(info)

    first_team = map_pick.current()[0] == 'team1'

    if request.method == 'POST':
        print('got to post')
        if 'map_pk' in request.POST:
            print('got to map_pk' + request.POST['map_pk'])
            print(first_team)
            if current[1] == 'pick':
                print('making a pick')
                map_pick.pick(request.POST['map_pk'], first_team)
            elif current[1] == 'ban':
                print('making a ban')
                map_pick.ban(request.POST['map_pk'], first_team)
        return redirect('map_pick', pk=map_pick.pk)

    if map_pick.current()[0] == 'done':
            return render(request, 'map_picker.html', {'maps': maps, 'mappick': map_pick, 'done': map_pick.picked})
    else:
        if first_team:
            team_turn = map_pick.team1
        else:
            team_turn = map_pick.team2

        if current[1] == 'pick':
            phase = 'picking'
        else:
            phase = 'banning'

        pick_line = team_turn + ' is ' + phase + '.'

    return render(request, 'map_picker.html', {'maps': maps, 'mappick': map_pick, 'pickline': pick_line, 'phase': phase})
