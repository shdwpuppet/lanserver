from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from .forms import MapPickForm
from .models import MapPick
import random


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
