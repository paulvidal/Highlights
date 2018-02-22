from raven.contrib.django.raven_compat.models import client
from django.core.management.base import BaseCommand

from fb_bot.model_managers import latest_highlight_manager
from highlights import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            highlights = latest_highlight_manager.get_all_highlights_without_info()

            for h in highlights:
                latest_highlight_manager.set_video_duration(h, -1)

        except Exception as error:
            if not settings.DEBUG:
                # Report to sentry if problem detected
                client.captureException()
            else:
                raise error