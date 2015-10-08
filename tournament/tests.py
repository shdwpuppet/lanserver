from django.test import TestCase
from tournament.models import *
from teams.models import Team
import datetime
import itertools



class RoundTest(TestCase):

    def create_tournament_setup(self):
        tournament = Tournament.objects.create(name='test tournament', slug='test', location='gxl', description='lalala', game='TF2', date_start=datetime.datetime.now(), date_end=datetime.datetime.now(), status='1')
        division = Division.objects.create(div_type=1, name='test div', slug='testdiv', tournament=tournament)
        group = division.create_group(name='Group A', inc_in_assignment=True)
        t1 = Team.objects.create(name='Team 1')
        t2 = Team.objects.create(name='Team 2')
        t3 = Team.objects.create(name='Team 3')
        t4 = Team.objects.create(name='Team 4')
        teams = [t1, t2, t3, t4]
        [division.assign_team_to_group(team) for team in teams]
        group.update_max_round()
        return {
            'tournament': tournament,
            'division': division,
            'group': group,
            'teams': teams,
        }

    def test_round_creation(self):
        setup = self.create_tournament_setup()
        group = setup['group']
        self.assertEqual(group.name, 'Group A')
        self.assertEqual(group.max_round, 3)
        for _ in itertools.repeat(None, group.max_round):
            group.start_round()

        matches = group.match_set.all()
        self.assertEqual(matches[0].home_team, setup['teams'][0])
        self.assertEqual(matches[0].away_team, setup['teams'][1])
        self.assertEqual(matches[1].home_team, setup['teams'][2])
        self.assertEqual(matches[1].away_team, setup['teams'][3])
        self.assertEqual(matches[2].home_team, setup['teams'][0])
        self.assertEqual(matches[2].away_team, setup['teams'][3])
        self.assertEqual(matches[3].home_team, setup['teams'][1])
        self.assertEqual(matches[3].away_team, setup['teams'][2])
        self.assertEqual(matches[4].home_team, setup['teams'][0])
        self.assertEqual(matches[4].away_team, setup['teams'][2])
        self.assertEqual(matches[5].home_team, setup['teams'][3])
        self.assertEqual(matches[5].away_team, setup['teams'][1])

    def test_round_creation_bye(self):
        setup = self.create_tournament_setup()
        group = setup['group']
        self.assertEqual(group.name, 'Group A')
        self.assertEqual(group.max_round, 3)
        group.teams.remove(group.teams.all()[3])
        self.assertEqual(group.teams.count(), 3)
        for _ in itertools.repeat(None, group.max_round):
            group.start_round()

        matches = group.match_set.all()
        self.assertEqual(matches[0].home_team, setup['teams'][0])
        self.assertEqual(matches[0].away_team, setup['teams'][1])
        self.assertEqual(matches[1].home_team, setup['teams'][2])
        self.assertEqual(matches[1].away_team, None)
        self.assertEqual(matches[2].home_team, setup['teams'][0])
        self.assertEqual(matches[2].away_team, None)
        self.assertEqual(matches[3].home_team, setup['teams'][1])
        self.assertEqual(matches[3].away_team, setup['teams'][2])
        self.assertEqual(matches[4].home_team, setup['teams'][0])
        self.assertEqual(matches[4].away_team, setup['teams'][2])
        self.assertEqual(matches[5].home_team, None)
        self.assertEqual(matches[5].away_team, setup['teams'][1])


