# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 10:48
from __future__ import unicode_literals

import audiofield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('audio_file', audiofield.fields.AudioField(blank=True, help_text=b'Allowed type - .mp3, .wav, .ogg', upload_to=b'your/upload/dir')),
            ],
        ),
    ]