# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-01 12:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0042_auto_20180518_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='newfootballregistration',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]