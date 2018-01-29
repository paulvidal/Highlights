from raven.contrib.django.raven_compat.models import client
from django.core.management.base import BaseCommand

from fb_bot.highlight_fetchers import fetcher_footyroom, fetcher_hoofoot
from highlights import settings


class ScrappingException(Exception):
    pass


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            highlights_footyroom = fetcher_footyroom.fetch_highlights(num_pagelet=1, max_days_ago=1000)

            if not highlights_footyroom:
                raise ScrappingException("Failed to scrape FOOTYROOM")

            highlights_hoofoot = fetcher_hoofoot.fetch_highlights(num_pagelet=1, max_days_ago=1000)

            if not highlights_hoofoot:
                raise ScrappingException("Failed to scrape HOOFOOT")

        except Exception as error:
            if not settings.DEBUG:
                # Report to sentry if problem detected
                client.captureException()
            else:
                raise error