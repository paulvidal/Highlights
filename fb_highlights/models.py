from __future__ import unicode_literals

from datetime import datetime

import dateparser
from django.contrib.postgres.fields import JSONField
from django.db import models

from fb_bot.highlight_fetchers.info import providers, sources


class User(models.Model):
    facebook_id = models.BigIntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    locale = models.CharField(max_length=10)
    timezone = models.SmallIntegerField()
    context = models.SmallIntegerField(default=1)
    see_result = models.BooleanField(default=True)

    # Stats
    join_date = models.DateTimeField(default=datetime.now)
    message_count = models.PositiveIntegerField(default=0)
    highlights_click_count = models.PositiveIntegerField(default=0)

    @staticmethod
    def to_list_display():
        return ['facebook_id', 'first_name', 'last_name', 'message_count', 'highlights_click_count', 'locale', 'join_date', 'context', 'see_result']

    @staticmethod
    def to_list_filter():
        return ['locale', 'see_result']

    @staticmethod
    def search_fields():
        return ['facebook_id', 'first_name', 'last_name', 'join_date']

    @staticmethod
    def get_default_user(facebook_id=0):
        return User(facebook_id=facebook_id,
                    first_name="user",
                    last_name="last",
                    locale="en_GB",
                    timezone=0)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)


class FootballTeam(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)

    @staticmethod
    def to_list_display():
        return ['name']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['name']

    def __str__(self):
        return str(self.name)


# Teams or competitions to potentially add
class NewFootballRegistration(models.Model):
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user", null=True, blank=True)
    time = models.DateTimeField(default=datetime.now)

    @staticmethod
    def to_list_display():
        return ['name', 'source', 'user', 'time']

    @staticmethod
    def to_list_filter():
        return ['source']

    @staticmethod
    def search_fields():
        return ['name']

    def __str__(self):
        return str(self.name) + ' | ' + str(self.source)


class FootballCompetition(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)

    @staticmethod
    def to_list_display():
        return ['name']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['name']

    def __str__(self):
        return str(self.name)


class RegistrationTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    team_name = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team_name")

    class Meta:
        unique_together = ('user', 'team_name')

    @staticmethod
    def to_list_display():
        return ['user', 'team_name']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['team_name__name', 'user__first_name']


class RegistrationCompetition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    competition_name = models.ForeignKey(FootballCompetition, on_delete=models.CASCADE, db_column="competition_name")

    class Meta:
        unique_together = ('user', 'competition_name')

    @staticmethod
    def to_list_display():
        return ['user', 'competition_name']

    @staticmethod
    def to_list_filter():
        return ['competition_name']

    @staticmethod
    def search_fields():
        return ['competition_name__name', 'user__first_name']


class LatestHighlight(models.Model):
    id = models.PositiveIntegerField()
    link = models.TextField(unique=True, primary_key=True)
    img_link = models.TextField(default="")
    time_since_added = models.DateTimeField()
    match_time = models.DateTimeField()
    category = models.ForeignKey(FootballCompetition, on_delete=models.CASCADE, db_column="category")
    view_count = models.IntegerField(default=0)
    team1 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team1", related_name="team1")
    score1 = models.SmallIntegerField()
    team2 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team2", related_name="team2")
    score2 = models.SmallIntegerField()
    source = models.CharField(max_length=80)
    type = models.CharField(max_length=80, default='normal')
    priority_short = models.PositiveIntegerField(default=0)
    priority_extended = models.PositiveIntegerField(default=0)
    sent = models.BooleanField(default=False)
    valid = models.BooleanField(default=True)
    ready = models.BooleanField(default=True)
    click_count = models.PositiveIntegerField(default=0)
    video_duration = models.IntegerField(default=0)
    video_url = models.TextField(null=True, blank=True)
    goal_data = JSONField(default=list, blank=True, null=True)

    @staticmethod
    def to_list_display():
        return ['id', 'link', 'match_time', 'time_since_added', 'team1', 'score1', 'team2', 'score2', 'category', 'video_duration', 'view_count', 'source', 'type', 'priority_short', 'priority_extended', 'sent', 'valid', 'ready', 'click_count', 'img_link', 'video_url']

    @staticmethod
    def to_list_filter():
        return ['category', 'source', 'type', 'sent', 'valid', 'ready']

    @staticmethod
    def search_fields():
        return ['id', 'link', 'team1__name', 'team2__name']

    def get_match_name(self):
        return "{} {} - {} {}".format(self.team1.name.title(), self.score1, self.score2, self.team2.name.title())

    def get_match_name_no_result(self):
        return "{} - {}".format(self.team1.name.title(), self.team2.name.title())

    def get_match_time(self):
        return self.match_time

    def get_parsed_time_since_added(self):
        return self.time_since_added

    def get_formatted_date(self):
        return self.get_parsed_time_since_added().strftime('%d %B %Y')

    def get_goals_elapsed(self):
        return [int(g['elapsed']) for g in self.goal_data]

    def provider_priority(self):
        priority = 0

        if providers.STREAMABLE in self.link:
            priority = 4

        elif providers.VEUCLIPS in self.link:
            priority = 4

        elif providers.VIUCLIPS in self.link:
            priority = 4

        elif providers.VIDSTREAM in self.link:
            priority = 4

        elif providers.TOCLIPIT in self.link:
            priority = 4

        elif providers.CLIPVENTURES in self.link:
            priority = 4

        elif providers.UPCLIPS in self.link:
            priority = 4

        elif providers.VIDSFORU in self.link:
            priority = 4

        elif providers.TO_STREAMIT in self.link:
            priority = 4

        elif providers.VIDEO_STREAMLET in self.link:
            priority = 4

        elif providers.CONTENT_VENTURES in self.link:
            priority = 4

        elif providers.DAILYMOTION in self.link:
            priority = 3

        elif providers.OK_RU in self.link:
            priority = 2

        elif providers.FOOYTROOM in self.link:
            priority = 1

        elif providers.YOUTUBE in self.link:
            priority = 1

        elif providers.MATCHAT_ONLINE in self.link:
            priority = 0

        return priority

    def __str__(self):
        return str(self.team1) + ' ' + str(self.score1) + ' - ' + str(self.score2) + ' ' + str(self.team2) + ' | ' + str(self.source)


class HighlightStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    match_id = models.PositiveIntegerField()
    team1 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team1", related_name="highlight_stat_team1")
    score1 = models.SmallIntegerField()
    team2 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team2", related_name="highlight_stat_team2")
    score2 = models.SmallIntegerField()
    link = models.TextField()
    time = models.DateTimeField()
    extended = models.BooleanField(default=False)
    video_duration = models.IntegerField(default=-2)

    class Meta:
        unique_together = ('user', 'time')

    @staticmethod
    def to_list_display():
        return ['user', 'match_id', 'team1', 'score1', 'team2', 'score2', 'time', 'link', 'extended', 'video_duration']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['user__first_name', 'team1__name', 'team2__name', 'match_id']


class HighlightNotificationStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    match_id = models.PositiveIntegerField()
    team1 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team1", related_name="highlight_notification_stat_team1")
    score1 = models.SmallIntegerField()
    team2 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team2", related_name="highlight_notification_stat_team2")
    score2 = models.SmallIntegerField()
    match_time = models.CharField(max_length=120)
    send_time = models.DateTimeField()
    open_time = models.DateTimeField(null=True, blank=True)
    opened = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'send_time')

    @staticmethod
    def to_list_display():
        return ['user', 'match_id', 'team1', 'score1', 'team2', 'score2', 'match_time', 'send_time', 'opened', 'open_time']

    @staticmethod
    def to_list_filter():
        return ['opened']

    @staticmethod
    def search_fields():
        return ['user__first_name', 'team1__name', 'team2__name', 'match_id']

    def get_parsed_match_time(self):
        return dateparser.parse(str(self.match_time))


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    match_id = models.PositiveIntegerField()
    team1 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team1", related_name="recommendation_team1")
    score1 = models.SmallIntegerField()
    team2 = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, db_column="team2", related_name="recommendation_team2")
    score2 = models.SmallIntegerField()
    match_time = models.DateTimeField()
    click_time = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'click_time')

    @staticmethod
    def to_list_display():
        return ['user', 'match_id', 'team1', 'score1', 'team2', 'score2', 'match_time', 'click_time']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['user__first_name', 'team1__name', 'team2__name']


class ScrappingStatus(models.Model):
    site_name = models.TextField(unique=True, primary_key=True)
    ok = models.BooleanField(default=True)

    @staticmethod
    def to_list_display():
        return ['site_name', 'ok']

    @staticmethod
    def to_list_filter():
        return ['ok']

    @staticmethod
    def search_fields():
        return ['site_name']


class ScraperApiKey(models.Model):
    code = models.TextField(unique=True, primary_key=True)
    last_invalid_try = models.DateTimeField(default=datetime.now)
    valid = models.BooleanField(default=True)
    mail = models.TextField(blank=True, null=True, default=None)
    password = models.TextField(blank=True, null=True, default=None)

    @staticmethod
    def to_list_display():
        return ['code', 'last_invalid_try', 'valid', 'mail', 'password']

    @staticmethod
    def to_list_filter():
        return ['valid']

    @staticmethod
    def search_fields():
        return ['code', 'mail']


class BlockedNotification(models.Model):
    team = models.ForeignKey(FootballTeam, on_delete=models.CASCADE, blank=True, null=True, default=None)
    competition = models.ForeignKey(FootballCompetition, on_delete=models.CASCADE, blank=True, null=True, default=None)

    class Meta:
        unique_together = ('team', 'competition')

    @staticmethod
    def to_list_display():
        return ['team', 'competition']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['team', 'competition']


class FootballTeamMapping(models.Model):
    team_name = models.CharField(max_length=200, db_column="team_name_mapping")
    team = models.ForeignKey(FootballTeam, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team_name', 'team')

    @staticmethod
    def to_list_display():
        return ['team_name', 'team']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['team_name', 'team__name']


class FootballCompetitionMapping(models.Model):
    competition_name = models.CharField(max_length=200, db_column="competition_name_mapping")
    competition = models.ForeignKey(FootballCompetition, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('competition_name', 'competition')

    @staticmethod
    def to_list_display():
        return ['competition_name', 'competition']

    @staticmethod
    def to_list_filter():
        return []

    @staticmethod
    def search_fields():
        return ['competition_name', 'competition__name']


class HighlightImage(models.Model):
    match_id = models.PositiveIntegerField()
    img_link = models.TextField(default="")
    img_uploaded_link = models.TextField(default="")
    source = models.CharField(max_length=80)

    class Meta:
        unique_together = ('match_id', 'img_link')

    def image_source_priority(self):
        priority = 0

        if sources.OUR_MATCH == self.source:
            priority = 4

        elif sources.HIGHLIGHTS_FOOTBALL == self.source:
            priority = 3

        elif sources.HOOFOOT == self.source:
            priority = 2

        elif sources.YOUTUBE == self.source:
            priority = 2

        elif sources.FOOTYROOM_VIDEOS == self.source or sources.FOOTYROOM == self.source:
            priority = 2

        elif sources.SPORTYHL == self.source:
            priority = 2

        return priority

    @staticmethod
    def to_list_display():
        return ['match_id', 'img_link', 'img_uploaded_link', 'source']

    @staticmethod
    def to_list_filter():
        return ['source']

    @staticmethod
    def search_fields():
        return ['match_id', 'img_link', 'img_uploaded_link']