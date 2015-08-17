from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)
    players = models.ManyToManyField(User, through='Player')
    
    def __str__(self):
        return self.name
    
class PlayerManager(models.Manager):
    use_for_related_fields = True
    
    def add_player(self, user, team, position):
        if Team.objects.filter(players__username=user.username):
            pass
        else:
            Player.objects.create(user=user, team=team, position=position)
        
    def remove_player(self, user, team):
        player = Player.objects.get(username=user)
        player.team=(None)
        player.save()
        
    def transfer_player(self, user, team):
        pass

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