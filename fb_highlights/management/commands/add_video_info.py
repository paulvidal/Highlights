from raven.contrib.django.raven_compat.models import client
from django.core.management.base import BaseCommand

from highlights import settings
from fb_bot import scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            scheduler.add_videos_info()
        except Exception as error:
            if not settings.DEBUG:
                # Report to sentry if problem detected
                client.captureException()
            else:
                raise error