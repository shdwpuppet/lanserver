# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.IntegerField(default=b'3', choices=[(1, b'Captain'), (2, b'Scheduler'), (3, b'Regular')]),
        ),
    ]
