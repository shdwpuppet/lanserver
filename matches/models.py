from django.db import models
from teams.models import Team


class Map(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home', null=True)
    away_team = models.ForeignKey(Team, related_name='away', null=True)
    map = models.ForeignKey(Map, null=True, blank=True)
    group = models.ForeignKey('tournament.Group', null=True)
    round = models.IntegerField(default=1)
    vetoes = models.IntegerField(default=2)
    home_veto = models.ManyToManyField(Map, related_name='home_veto', null=True)
    away_veto = models.ManyToManyField(Map, related_name='away_veto', null=True)
    server = models.ForeignKey('tournament.Server', null=True)
    veto_turn = models.IntegerField(default=0)


class Result(models.Model):
    match = models.OneToOneField(Match, null=True, blank=True)
    winner = models.ForeignKey(Team, related_name='winner')
    loser = models.ForeignKey(Team, related_name='loser', null=True, blank=True)
    winner_rf = models.IntegerField()
    winner_ra = models.IntegerField()
    loser_rf = models.IntegerField()
    loser_ra = models.IntegerField()
    is_tie = models.BooleanField(default=False)
    is_bye = models.BooleanField(default=False)

    def record_result(self, t1, s1, t2=None, s2=None, is_bye=False):
        if not is_bye:
            if s1 > s2:
                self.winner = t1
                self.loser = t2
                self.winner_rf = s1
                self.winner_ra = s2
                self.loser_rf = s2
                self.loser_ra = s1

            elif s1 < s2:
                self.winner = t2
                self.loser = t1
                self.winner_rf = s2
                self.winner_ra = s1
                self.loser_rf = s1
                self.loser_ra = s2
            else:  # score must be tied
                self.winner = None
                self.loser = None
                self.winner_ra = s1
                self.loser_ra = s2
                self.winner_rf = s2
                self.loser_rf = s1
                self.is_tie = True
            self.save()
        else:  # is bye
            self.winner = t1
            self.loser = None
            self.winner_rf = s1
            self.winner_ra = 0
            self.loser_rf = 0
            self.loser_ra = 0
            self.save()
