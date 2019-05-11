# Generated by Django 2.2.1 on 2019-05-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0061_footballcompetitionmapping_footballteammapping'),
    ]

    operations = [
        migrations.CreateModel(
            name='HighlightImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.PositiveIntegerField()),
                ('img_link', models.TextField(default='')),
                ('img_uploaded_link', models.TextField(default='')),
                ('source', models.CharField(max_length=80)),
            ],
            options={
                'unique_together': {('match_id', 'img_link')},
            },
        ),
    ]
