from django.db import models
from teams.models import Team


class Map(models.Model):
    name=models.CharField(max_length=64)


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home')
    away_team = models.ForeignKey(Team, related_name='away')
    map = models.ForeignKey(Map)

class Result(models.Model):
    match = models.ForeignKey(Match)
    winner = models.ForeignKey(Team, related_name='winner')
    loser = models.ForeignKey(Team, related_name='loser')
    winner_rf = models.IntegerField()
    winner_ra = models.IntegerField()
    loser_rf = models.IntegerField()
    loser_ra = models.IntegerField()
    is_tie = models.BooleanField(default=False)
    is_bye = models.BooleanField(default=False)

    def record_result(self, t1, t2=None, s1, s2=None, is_bye=False):
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
            self.loser_ra = s1
            self.save()
