from django.test import TestCase
from django.contrib.auth.models import User
from teams.models import Team, Player

# Create your tests here.


class TeamTest(TestCase):

    def create_team(self, name="test team"):
        return Team.objects.create(name=name)

    def create_user(self, name="test user", email="test@test.test", password="password"):
        return User.objects.create_user(name, email, password)

    def test_add_player(self):
        u = self.create_user()
        t = self.create_team()
        Player.objects.add_player(u, t, 3)
        pt = Team.objects.filter(players__username='test user')
        ut = User.objects.filter(team__name="test team")
        self.assertIn(t, pt)
        self.assertIn(u, ut)
        self.assertNotIn(u, t.get_captains())

    def test_add_captain(self):
        u = self.create_user()
        t = self.create_team()
        p = Player.objects.add_player(u, t, 1)
        pt = Team.objects.filter(players__username='test user')
        ut = User.objects.filter(team__name="test team")
        self.assertIn(t, pt)
        self.assertIn(u, ut)
        self.assertIn(p, t.get_captains())

    def test_remove_player(self):
        u = self.create_user()
        t = self.create_team()
        Player.objects.add_player(u, t, 1)
        pt = Team.objects.filter(players__username='test user')
        self.assertIn(t, pt)
        Player.objects.remove_player(u)
        pt = Team.objects.filter(players__username='test user')
        self.assertNotIn(t, pt)

    def test_transfer_player(self):
        u = self.create_user()
        t = self.create_team()
        Player.objects.add_player(u, t, 3)
        pt = Team.objects.filter(players__username='test user')
        ut = User.objects.filter(team__name="test team")
        self.assertIn(t, pt)
        self.assertIn(u, ut)
        t2 = self.create_team(name="test2")
        Player.objects.transfer_player(u, t2)
        pt = Team.objects.filter(players__username='test user')
        ut = User.objects.filter(team__name="test team")
        pt2 = Team.objects.filter(players__username='test user')
        ut2 = User.objects.filter(team__name="test2")
        self.assertNotIn(t, pt)
        self.assertIn(t2, pt2)
        self.assertNotIn(u, ut)
        self.assertIn(u, ut2)

    def test_create_team(self):
        t = self.create_team()
        self.assertTrue(isinstance(t, Team))
        self.assertEqual(t.name, "test team")
