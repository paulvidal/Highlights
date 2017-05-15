from django.core.management.base import BaseCommand

from fb_bot import scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler.send_most_recent_highlights()
