from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)
    players = models.ManyToManyField(User, through='Player')
    join_pass = models.CharField(max_length=50)
    description = models.TextField()
    website = models.CharField(max_length=240)

    def get_captains(self):
        return Player.objects.filter(team=self, position=1)

    def change_captain(self, new_captain):
        for player in self.get_captains():
            player.position = 3
            player.save()
        new_captain.position = 1

    def __str__(self):
        return self.name

    def get_all_matches(self):
        return self.home.all() | self.away.all()

    def get_overall_record(self):
        return{
            'wins': len(self.winner.all()),
            'loss': len(self.loser.all()),
        }
    
    class Meta:
        managed = True


class PlayerManager(models.Manager):
    use_for_related_fields = True

    def add_player(self, user, team, position):
        if Team.objects.filter(players__username=user.username):
            pass
        else:
            player = Player.objects.create(user=user, team=team, position=position)
        if len(Player.objects.filter(team=team)) == 1:
            player.position = 1
            player.save()
        return player

    def remove_player(self, user):
        player = Player.objects.filter(user=user)
        [player.delete() for player in player]

    def transfer_player(self, user, new_team):
        self.remove_player(user)
        self.add_player(user, new_team, 3)


class Player(models.Model):
    PLAYER_ROLES = (
        (1, 'Captain'),
        (2, 'Scheduler'),
        (3, 'Regular')
    )

    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    position = models.IntegerField(choices=PLAYER_ROLES, default='3')
    objects = PlayerManager()
