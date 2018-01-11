from raven.contrib.django.raven_compat.models import client
from django.core.management.base import BaseCommand

from highlights import settings
from fb_bot import scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            scheduler.send_most_recent_highlights()
        except:
            # Report to sentry if problem detected
            if not settings.DEBUG:
                client.captureException()