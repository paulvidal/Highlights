# Generated by Django 2.2.1 on 2019-05-05 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fb_highlights', '0058_auto_20190129_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='newfootballregistration',
            name='user',
            field=models.ForeignKey(blank=True, db_column='user', null=True, on_delete=django.db.models.deletion.CASCADE, to='fb_highlights.User'),
        ),
    ]
