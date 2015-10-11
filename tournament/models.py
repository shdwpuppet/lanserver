from django.db import models
from teams.models import Team
from django.db.models import Count
from django.utils.text import slugify
from matches.models import Match
from map.models import Map


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
    map_pool = models.ManyToManyField(Map)

    class Meta:
        managed = True
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
    num_finalists = models.IntegerField(default=2)  # number of teams that move from group stage to brackets
    is_open = models.BooleanField(default=True)

    def get_assignable_groups(self):
        return Group.objects.all().annotate(teams_count=Count('teams')).order_by('-teams_count').filter(division=self).reverse()

    def assign_team_to_group(self, team, group=None):
        if group is None:
            group = self.get_assignable_groups()[0]
            group.teams.add(team)
            group.update_max_round()
        else:
            group.teams.add(team)
            group.max_round = (group.teams.count() - 1)
            group.update_max_round()
        Record.objects.create(team=team, group=group, )

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
        return group

    def start_playoffs(self):
        if all(finished is True for finished in [group.is_finished for group in self.group_set.all()]):
            pass


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
    current_round = models.IntegerField(default=1)
    max_round = models.IntegerField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_fixtures(self):
        teams = list(self.teams.all())
        if len(teams) % 2:
            teams.append(None)
        rotation = list(teams)
        fixtures = []
        for i in range(0, len(teams) - 1):
            fixtures.append(rotation)
            rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
        return fixtures

    def update_record(self, match):
        pass

    def update_max_round(self):
        if self.teams.count() < 2:
            self.max_round = 1
        else:
            self.max_round = self.teams.count() - 1
            self.save()

    def update_ranks(self):
        records = self.record_set.order_by('win', 'loss', 'rf')
        ct = 0
        for record in records[::-1]:
            rank = self.rank_set.filter(team=record.team)[0]
            rank.rank = len(records) - ct
            rank.save()
            ct += 1

    def start_round(self):
        if self.current_round <= self.max_round:
            # get the fixtures, find the round, assign the matches.
            fixtures = self.get_fixtures()
            this_round = fixtures[self.current_round]
            for i in range(0, len(this_round), 2):
                teams = this_round[i:i+2]
                Match.objects.create(home_team=teams[0], away_team=teams[1], group=self, round=self.current_round)
            self.current_round += 1
            self.save()

        else:  # all matches in this game have been played, set the group to finished and check if they are all finished at the div level
            self.is_finished = True
            self.save()


class Bracket(models.Model):
    division = models.OneToOneField(Division)


class Seed(models.Model):
    bracket = models.ForeignKey(Bracket)
    team = models.ForeignKey(Team)
    seed = models.IntegerField()


class Record(models.Model):
    group = models.ForeignKey(Group)
    team = models.ForeignKey(Team)
    win = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    rf = models.IntegerField(default=0)
    ra = models.IntegerField(default=0)

    def record_match(self, rf, ra):
        if rf > ra:
            self.win += 1
        else:
            self.loss += 1
        self.rf += rf
        self.ra += ra


class Server(models.Model):
    name = models.CharField(max_length=64)
    ip = models.CharField(max_length=20)
    is_in_use = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Rank(models.Model):
    team = models.ForeignKey(Team)
    rank = models.IntegerField()
    group = models.ForeignKey(Group)



