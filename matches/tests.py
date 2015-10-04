from django.test import TestCase
from teams.models import Team
from matches.models import Map, Match, Result


class MatchTest(TestCase):

    def create_teams(self):
        t1 = Team.objects.create(name='Home Team')
        t2 = Team.objects.create(name='Away Team')
        return [t1, t2]

    def add_map(self):
        return Map.objects.create(name="cp_granary")

    def create_match(self):
        teams = self.create_teams()
        return Match.objects.create(home_team=teams[0], away_team=teams[1], map=self.add_map())

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


