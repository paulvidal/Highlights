# Generated by Django 2.1.2 on 2019-01-29 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0056_auto_20181117_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score1', models.SmallIntegerField()),
                ('score2', models.SmallIntegerField()),
                ('match_time', models.DateTimeField()),
                ('click_time', models.DateTimeField()),
                ('team1', models.ForeignKey(db_column='team1', on_delete=django.db.models.deletion.CASCADE, related_name='recommendation_team1', to='fb_highlights.FootballTeam')),
                ('team2', models.ForeignKey(db_column='team2', on_delete=django.db.models.deletion.CASCADE, related_name='recommendation_team2', to='fb_highlights.FootballTeam')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='fb_highlights.User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='recommendation',
            unique_together={('user', 'click_time')},
        ),
    ]
