# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-25 01:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20151224_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='telegram_id',
            field=models.CharField(blank=True, default=b'', max_length=255),
        ),
    ]