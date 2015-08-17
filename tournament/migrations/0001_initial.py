# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_player_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_visible', models.BooleanField()),
                ('teams', models.ManyToManyField(to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home_score', models.IntegerField()),
                ('away_score', models.IntegerField()),
                ('is_bye', models.BooleanField()),
                ('away_team', models.ForeignKey(related_name='away_team', to='teams.Team')),
                ('division', models.ForeignKey(to='tournament.Division')),
                ('home_team', models.ForeignKey(related_name='home_team', to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('win', models.IntegerField()),
                ('loss', models.IntegerField()),
                ('tie', models.IntegerField()),
                ('rf', models.IntegerField()),
                ('ra', models.IntegerField()),
                ('difficulty_of_schedule', models.DecimalField(max_digits=5, decimal_places=3)),
                ('rank', models.IntegerField()),
                ('division', models.ForeignKey(to='tournament.Division')),
                ('team', models.ForeignKey(to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='division',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament'),
        ),
    ]
