# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-21 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0025_auto_20180220_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='latesthighlight',
            name='video_duration',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='latesthighlight',
            name='video_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
