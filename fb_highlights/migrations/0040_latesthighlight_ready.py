# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-13 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0039_auto_20180510_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='latesthighlight',
            name='ready',
            field=models.BooleanField(default=True),
        ),
    ]
