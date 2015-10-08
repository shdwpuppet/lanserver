from django.test import TestCase
from teams.models import Team
from matches.models import Map, Match, Result
from tournament.models import Group, Tournament, Division
import datetime


class MatchTest(TestCase):

    def create_tournament_setup(self):
        tournament = Tournament.objects.create(name='test tournament', slug='test', location='gxl', description='lalala', game='TF2', date_start=datetime.datetime.now(), date_end=datetime.datetime.now(), status='1')
        division = Division.objects.create(div_type=1, name='test div', slug='testdiv', tournament=tournament)
        group = division.create_group(name='Group A', inc_in_assignment=True)

        return {
            'tournament': tournament,
            'division': division,
            'group': group
        }

    def create_teams(self):
        t1 = Team.objects.create(name='Home Team')
        t2 = Team.objects.create(name='Away Team')
        return [t1, t2]

    def add_map(self):
        return Map.objects.create(name="cp_granary")

    def create_match(self):
        teams = self.create_teams()
        tournament = self.create_tournament_setup()
        return Match.objects.create(home_team=teams[0], away_team=teams[1], map=self.add_map(), group=tournament['group'])

    def test_home_win(self):
        match = self.create_match()
        record = Result()
        record.match = match
        record.record_result(t1=match.home_team, t2=match.away_team, s1=5, s2=3)
        self.assertEqual(record.winner, match.home_team)
        self.assertEqual(record.loser, match.away_team)
        self.assertEqual(record.winner_rf, 5)
        self.assertEqual(record.winner_ra, 3)
        self.assertEqual(record.loser_ra, 5)
        self.assertEqual(record.loser_rf, 3)

    def test_away_win(self):
        match = self.create_match()
        record = Result()
        record.match = match
        record.record_result(t1=match.home_team, t2=match.away_team, s1=3, s2=5)
        self.assertEqual(record.winner, match.away_team)
        self.assertEqual(record.loser, match.home_team)
        self.assertEqual(record.winner_rf, 5)
        self.assertEqual(record.winner_ra, 3)
        self.assertEqual(record.loser_ra, 5)
        self.assertEqual(record.loser_rf, 3)

    def test_bye(self):
        match = self.create_match()
        record = Result()
        record.match = match
        record.is_bye = True
        record.record_result(t1=match.home_team, s1=3, is_bye=True)
        record.save()
        self.assertEqual(record.is_bye, True)
        self.assertEqual(record.winner, match.home_team)
        self.assertEqual(record.loser, None)
        self.assertEqual(record.winner_rf, 3)
        self.assertEqual(record.winner_ra, 0)


