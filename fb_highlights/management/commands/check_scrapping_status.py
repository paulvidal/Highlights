from raven.contrib.django.raven_compat.models import client
from django.core.management.base import BaseCommand

from fb_bot import scheduler
from highlights import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            scheduler.check_scrapping_status()
        except Exception as error:
            if not settings.DEBUG:
                # Report to sentry if problem detected
                client.captureException()
            else:
                raise error