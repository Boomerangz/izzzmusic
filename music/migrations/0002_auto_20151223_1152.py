# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 11:52
from __future__ import unicode_literals

import audiofield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='album',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='track',
            name='artist',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AddField(
            model_name='track',
            name='title',
            field=models.CharField(default=b'', max_length=255),
        ),
        migrations.AlterField(
            model_name='track',
            name='audio_file',
            field=audiofield.fields.AudioField(blank=True, help_text=b'Allowed type - .mp3, .wav, .ogg', upload_to=b'music'),
        ),
    ]
