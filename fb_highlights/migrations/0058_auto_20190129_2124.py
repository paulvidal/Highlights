# Generated by Django 2.1.2 on 2019-01-29 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0057_auto_20190129_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='highlightnotificationstat',
            name='match_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='highlightstat',
            name='match_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recommendation',
            name='match_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
