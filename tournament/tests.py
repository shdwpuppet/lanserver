from django.test import TestCase
from tournament.models import Tournament, Division, RRGroup
from teams.models import Team
from django.db.models import Count

# Create your tests here.


class TournamentTest(TestCase):

    def create_tournament(self, name="test tournament", slug="This is a test tournament"):
        return Tournament.objects.create(name=name, slug=slug)

    def create_team(self, name='test team'):
        return Team.objects.create(name=name)

    def create_RRGroup(self, name, division, assignable):
        return RRGroup.objects.create(name=name, division=division, inc_in_assignment=assignable)

    def create_division(div_type, tournament, name="Test Div", slug=""):
        return Division.objects.create(div_type=div_type, name=name, slug=slug, tournament=tournament)

    def test_create_tournament(self):
        t = self.create_tournament()
        self.assertEqual(t.name, "test tournament")

    def test_add_teams_to_groups(self):
        team1 = self.create_team(name="team1")
        team2 = self.create_team(name="team2")
        team3 = self.create_team(name="team3")
        t = self.create_tournament()
        d = Division.objects.create(div_type=1, name="test div", slug="", tournament=t)
        r1 = self.create_RRGroup(name="A", division=d, assignable=True)
        r2 = self.create_RRGroup(name="B", division=d, assignable=True)
        d.assign_team_to_rrgroup(team=team1, group=r1)
        self.assertIn(team1, r1.teams.all())
        print(d.get_assignable_groups())
        d.assign_team_to_rrgroup(team=team2)
        print(r2.teams.all())
        self.assertIn(team2, r2.teams.all())