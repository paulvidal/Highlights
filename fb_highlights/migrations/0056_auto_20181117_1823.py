# Generated by Django 2.1.2 on 2018-11-17 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0055_auto_20181115_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='fb_highlights.FootballCompetition')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fb_highlights.FootballTeam')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='deniedforcompetitionhighlight',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='deniedforcompetitionhighlight',
            name='competition',
        ),
        migrations.RemoveField(
            model_name='deniedforcompetitionhighlight',
            name='team',
        ),
        migrations.DeleteModel(
            name='DeniedForCompetitionHighlight',
        ),
        migrations.AlterUniqueTogether(
            name='blockednotification',
            unique_together={('team', 'competition')},
        ),
    ]
