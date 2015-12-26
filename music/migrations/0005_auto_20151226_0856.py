# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_track_telegram_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='audio_file',
        ),
        migrations.AddField(
            model_name='track',
            name='duration',
            field=models.IntegerField(default=300, max_length=255, blank=True),
        ),
    ]
