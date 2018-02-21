import dateparser
from django.core.management.base import BaseCommand

from fb_bot.model_managers import highlight_stat_manager, highlight_notification_stat_manager


class Command(BaseCommand):

    def handle(self, *args, **options):
        highlight_stats = highlight_stat_manager.get_all_highlight_stats()
        highlight_notification_stats = highlight_notification_stat_manager.get_all_highlight_notification_stats()

        for h in highlight_stats:
            h.time_2 = dateparser.parse(h.time)
            h.save()

        for h in highlight_notification_stats:
            print(dateparser.parse(h.send_time))

            h.send_time_2 = dateparser.parse(h.send_time)
            h.open_time_2 = dateparser.parse(h.open_time)
            h.save()