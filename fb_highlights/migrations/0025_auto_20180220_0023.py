# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-20 00:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0024_auto_20180220_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlightstat',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 20, 0, 23, 15, 735114)),
            preserve_default=False,
        ),
    ]
