from django.db import models
from teams.models import Team
from django.db.models import Count
from django.utils.text import slugify


class Tournament(models.Model):
    ROSTERS_OPEN = 1
    ROSTERS_LOCKED = 2
    ENDED = 3
    HIDDEN = 4
    STATUS =(
        (ROSTERS_OPEN, 'Rosters Open'),
        (ROSTERS_LOCKED, 'Rosters Locked'),
        (ENDED, 'Ended'),
        (HIDDEN, 'Hidden'),
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    game = models.TextField(max_length=50)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.IntegerField(choices=STATUS, default='1')

    class Meta:
        verbose_name = "Tournaments"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here

    def signup(self, team, requested_div):
        Signup.objects.create(team=team, tournament=self, requested_div=requested_div)

    def add_division(self, dtype, name, num_finalists):
        slug = slugify(name)
        d = Division.objects.create(div_type=dtype, name=name, slug=slug, tournament=self, num_finalists=num_finalists)
        d.save()


class Division(models.Model):

    TYPES = (
        (1, 'RR'),
        (2, 'LEAGUE'),
    )
    div_type = models.IntegerField(choices=TYPES, default='1')
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    tournament = models.ForeignKey(Tournament)
    num_finalists = models.IntegerField(default=2) # number of teams that move from group stage to brackets
    is_open = models.BooleanField(default=True)

    def get_assignable_groups(self):
        return Group.objects.all().annotate(teams_count=Count('teams')).order_by('-teams_count').filter(division=self).filter(inc_in_assignment=True).reverse()

    def assign_team_to_group(self, team, group=None):
        if group is None:
            group = self.get_assignable_groups()[0]
            group.teams.add(team)
        else:
            group.teams.add(team)
        group.max_round = group.teams.count() - 1

    def remove_team_from_group(self, team, group):
        group.teams.remove(team)
        group.save()

    def move_up(self):
        for group in self.group_set.all():
            pass

    def join(self, team):
        pass

    def create_group(self, name, inc_in_assignment):
        group = Group()
        group.name = name
        group.inc_in_assignment = inc_in_assignment
        group.division = self
        group.current_round = 0
        group.max_round = 0
        group.save()

    class Meta:
        verbose_name = "Division"
        verbose_name_plural = "Divisions"

    def __str__(self):
        return self.name


class Signup(models.Model):
    team = models.ForeignKey(Team)
    tournament = models.ForeignKey(Tournament)
    requested_div = models.ForeignKey(Division)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('team', 'tournament')


class Group(models.Model):
    division = models.ForeignKey(Division)
    name = models.CharField(max_length=50)
    teams = models.ManyToManyField(Team)
    # should this group be included in the automatic inc_in_assignment
    inc_in_assignment = models.BooleanField()
    current_round = models.IntegerField()
    max_round = models.IntegerField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Bracket(models.Model):
    division = models.OneToOneField(Division)


class Seed(models.Model):
    bracket = models.ForeignKey(Bracket)
    team = models.ForeignKey(Team)
    seed = models.IntegerField()


class Rank(models.Model):
    team = models.ForeignKey(Team)
    rank = models.IntegerField()
    group = models.ForeignKey(Group)
