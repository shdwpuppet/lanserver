from django.db import models

# Create your models here.

class Tournament(models.Model):
    RR_DE = 1
    RR_SE = 2
    LG_DE = 3
    LG_SE = 4
    TYPE_CHOICES = (
        (RR_DE, 'Round Robin with Double Elimination Finals'),
        (RR_SE, 'Round Robin with Single Elimination'),
        (LG_DE, 'League with Double Elimination Finals'),
        (LG_SE, 'League with Single Elimination'),
    )
    name = models.CharField(max_length = 64)
    description = models.TextField()
    t_type = models.IntegerField(choices=TYPE_CHOICES, default=RR_DE)
   
    def create_div(self, visible=False):
        Division.objects.create(tournament=self, is_visible=visible) 
    
    def add_team(team, division=None):
        pass #chooses a division to add them to depending on type of tournament
    
    def start_finals():
        pass #finalizes the brackets, adds the top x teams from each division
class Division(models.Model):
    tournament = models.ForeignKey('Tournament')
    #div_type = round robin, 
    is_visible = models.BooleanField() #is it to be shown yet in the public facing areas
    teams = models.ManyToManyField('teams.Team')
    
class Record(models.Model):
    division = models.ForeignKey('Division')
    team = models.ForeignKey('teams.Team')
    win = models.IntegerField()
    loss = models.IntegerField()
    tie = models.IntegerField()
    rf = models.IntegerField()
    ra = models.IntegerField()
    difficulty_of_schedule = models.DecimalField(max_digits=5, decimal_places=3)
    rank = models.IntegerField()
    
    def recalculate_dos():
        #recalculate the difficulty of schedule
        pass
        
class Match(models.Model):
    division = models.ForeignKey('Division')
    home_team = models.ForeignKey('teams.Team', related_name='home_team')
    away_team = models.ForeignKey('teams.Team', related_name='away_team')
    gmap = models.CharField(max_length = 64, default='cp_snakewater')
    #winning side is gotten by finding difference in scores
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    is_bye = models.BooleanField()
    #status = choice between status fields. The controller will hook into this database table and lookup pending statuses to set up the server with

    def create_match(home, away, is_bye, div):
      pass  

    def get_winner():
        pass
        #return the winner, decided by comparing homse score vs away score
        if not is_bye:
            if home_score > away_score:
                return 'home'
            elif away_score > home_score:
                return 'away'
            elif away_score == home_score:
                return 'tie'
                
    def record_match(self):
        hr = Record.objects.filter(team = home_team).filter(division = self.division)
        ar = Record.objects.filter(team = home_team).filter(division = self.division)
        
        hr.rf = hr.rf + home_score
        ar.rf = ar.rf + away_score        
        hr.ra = hr.ra + away_score
        ar.ra = ar.ra + home_score
        
        if get_winner() == 'home':
            hr.win = hr.win +1
            ar.loss = ar.loss +1
        elif get_winner() == 'away':
            ar.win = ar.win +1
            hr.loss = hr.loss +1
        elif get_winner() == 'tie':
            hr.tie = hr.tie + 1
            ar.tie = ar.tie + 1
        
    def change_record():
        pass
        #calculate the difference in scores, then add that difference into the scores
        