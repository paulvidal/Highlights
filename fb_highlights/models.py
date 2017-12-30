from __future__ import unicode_literals

from datetime import datetime

import dateparser
from django.db import models

from fb_bot.highlight_fetchers import football_team_mapping


class User(models.Model):
    facebook_id = models.BigIntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    image_url = models.URLField(max_length=200)
    locale = models.CharField(max_length=10)
    timezone = models.SmallIntegerField()
    gender = models.CharField(max_length=20)
    context = models.SmallIntegerField(default=1)

    # Stats
    join_date = models.DateTimeField(default=datetime.now)
    message_count = models.PositiveIntegerField(default=0)

    @staticmethod
    def to_list_display():
        return 'facebook_id', 'first_name', 'last_name', 'image_url', 'gender', 'message_count', 'join_date', 'context'

    @staticmethod
    def to_list_filter():
        return 'gender', 'locale'

    @staticmethod
    def search_fields():
        return 'facebook_id', 'first_name', 'last_name', 'join_date'

    @staticmethod
    def get_default_user():
        return User(facebook_id=0,
                    first_name="man",
                    last_name="",
                    image_url="",
                    locale="",
                    timezone=0,
                    gender="")

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class FootballTeam(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)

    @staticmethod
    def to_list_display():
        return 'name',

    @staticmethod
    def to_list_filter():
        return ()

    @staticmethod
    def search_fields():
        return 'name',

    def __str__(self):
        return str(self.name)


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    team_name = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team_name")

    class Meta:
        unique_together = ('user', 'team_name')

    @staticmethod
    def to_list_display():
        return 'user', 'team_name'

    @staticmethod
    def to_list_filter():
        return ()

    @staticmethod
    def search_fields():
        return 'team_name',


class LatestHighlight(models.Model):
    link = models.TextField(unique=True, primary_key=True)
    img_link = models.TextField(default="")
    time_since_added = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    view_count = models.IntegerField(default=0)
    team1 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team1", related_name="team1")
    score1 = models.SmallIntegerField()
    team2 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team2", related_name="team2")
    score2 = models.SmallIntegerField()
    source = models.CharField(max_length=80)
    sent = models.BooleanField(default=False)

    @staticmethod
    def to_list_display():
        return 'link', 'img_link', 'time_since_added', 'team1', 'score1', 'team2', 'score2', 'category', 'view_count', 'source', 'sent'

    @staticmethod
    def to_list_filter():
        return 'category', 'source', 'sent'

    @staticmethod
    def search_fields():
        return 'team1__name', 'team2__name'

    def get_match_name(self):
        return "{} {} - {} {}".format(self.team1.name.title(), self.score1, self.score2, self.team2.name.title())

    def get_parsed_time_since_added(self):
        return dateparser.parse(str(self.time_since_added))

    def is_match_of(self, team_name):
        """
        :param team_name: the name of the football team
        :return: True if the highlight is for a match with this team
        """
        team_name = football_team_mapping.get_exact_name(team_name.lower())
        return self.team1.name.startswith(team_name) or self.team2.name.startswith(team_name)