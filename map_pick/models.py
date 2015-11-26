from django.db import models
from map.models import Map
import random

class MapPick(models.Model):
    map_pool = models.ManyToManyField(Map)
    team1 = models.CharField(max_length=64)
    team2 = models.CharField(max_length=64)
    stage = models.IntegerField(default=0)
    order = models.CharField(max_length=128, default='team1_ban,team2_ban,team1_pick,team2_pick,team1_ban,team2_ban,default_pick,done_done')
    picked = models.CharField(max_length=128, default='')

    def pick(self, map, first_team):
        map = Map.objects.get(pk=map)
        if first_team:
            team = self.team1
        else:
            team = self.team2
        Pick.objects.create(mappick=self, map=map, team=team)
        self.picked += (' ' + map.name)
        self.stage += 1
        self.save()

    def last_pick(self):
        # randomly pick from the remaining maps, ban the rest
        pick = random.choice(self.maps_left())
        Pick.objects.create(mappick=self, map=pick, team='default')
        self.picked += (' ' + pick.name)
        [Ban.objects.create(mappick=self, map=mp, team='default') for mp in self.maps_left()]
        self.stage += 1
        self.save()

    def ban(self, map, first_team):
        map = Map.objects.get(pk=map)
        if first_team:
            team = self.team1
        else:
            team = self.team2
        Ban.objects.create(mappick=self, map=map, team=team)
        self.stage += 1
        self.save()

    def current(self):
        order = self.order.split(',')
        return order[self.stage].split('_')  # returns a list [team, phase]

    def map_banned(self, map_pk):
        map = Map.objects.get(pk=map_pk)
        return self.ban_set.filter(map=map).exists()

    def map_banned_by(self, map_pk):
        if self.map_banned(map_pk):
            return self.ban_set.filter(map=Map.objects.get(pk=map_pk))[0].team

    def map_picked_by(self, map_pk):
        if self.map_picked(map_pk):
            return self.pick_set.filter(map=Map.objects.get(pk=map_pk))[0].team

    def map_picked(self, map_pk):
        map = Map.objects.get(pk=map_pk)
        return self.pick_set.filter(map=map).exists()

    def maps_left(self):
        banned_maps = [ban.map for ban in self.ban_set.all()]
        picked_maps = [pick.map for pick in self.pick_set.all()]
        return [map for map in self.map_pool.all() if map not in (banned_maps+picked_maps)]





class Ban(models.Model):
    mappick = models.ForeignKey(MapPick)
    map = models.ForeignKey(Map)
    team = models.CharField(max_length=64)

    class Meta:
        unique_together = ('mappick', 'map')


class Pick(models.Model):
    mappick = models.ForeignKey(MapPick)
    map = models.ForeignKey(Map)
    team = models.CharField(max_length=64)

    class Meta:
        unique_together = ('mappick', 'map')
