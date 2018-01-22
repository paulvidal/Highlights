from raven.contrib.django.raven_compat.models import client
from django.core.management.base import BaseCommand

from fb_bot.highlight_fetchers import footyroom_fetcher, hoofoot_fetcher
from highlights import settings


class ScrappingException(Exception):
    pass


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            highlights_footyroom = footyroom_fetcher.fetch_highlights(num_pagelet=1, max_days_ago=1000)

            if not highlights_footyroom:
                raise ScrappingException("Failed to scrape FOOTYROOM")

            highlights_hoofoot = hoofoot_fetcher.fetch_highlights(num_pagelet=1, max_days_ago=1000)

            if not highlights_hoofoot:
                raise ScrappingException("Failed to scrape HOOFOOT")

        except Exception as error:
            if not settings.DEBUG:
                # Report to sentry if problem detected
                client.captureException()
            else:
                raise error