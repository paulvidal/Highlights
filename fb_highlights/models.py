from __future__ import unicode_literals

from datetime import datetime

from django.db import models


class User(models.Model):
    facebook_id = models.BigIntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    image_url = models.URLField(max_length=200)
    locale = models.CharField(max_length=10)
    timezone = models.SmallIntegerField()
    gender = models.CharField(max_length=20)

    # Stats
    join_date = models.DateTimeField(default=datetime.now)
    message_count = models.PositiveIntegerField(default=0)

    @staticmethod
    def to_list_display():
        return 'facebook_id', 'first_name', 'last_name', 'image_url', 'gender', 'message_count', 'join_date'

    @staticmethod
    def to_list_filter():
        return 'gender', 'locale'

    @staticmethod
    def search_fields():
        return 'facebook_id', 'first_name', 'last_name', 'join_date'

    @staticmethod
    def get_default_user():
        return User(facebook_id=0,
                    first_name="Default",
                    last_name="",
                    image_url="",
                    locale="",
                    timezone=0,
                    gender="")

    def __str__(self):
        return str((self.facebook_id, self.first_name, self.last_name, self.image_url, self.locale, self.timezone, self.gender))
