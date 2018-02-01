from django.core.management.base import BaseCommand

from fb_bot.highlight_fetchers import mapping_football_team, mapping_football_competition
from fb_bot.model_managers import football_team_manager, latest_highlight_manager


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_highlights = latest_highlight_manager.get_all_highlights()

        for h in all_highlights:
            h.category = mapping_football_competition.get_exact_name(h.category.lower())
            h.save()