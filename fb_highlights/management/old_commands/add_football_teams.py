from django.core.management.base import BaseCommand

from fb_bot.highlight_fetchers import fetcher_footyroom
from fb_bot.model_managers import football_team_manager


class Command(BaseCommand):

    def handle(self, *args, **options):
        highlights = fetcher_footyroom.fetch_highlights(100, 1000)

        for highlight in highlights:
            football_team_manager.add_football_team(highlight.team1.lower())
            football_team_manager.add_football_team(highlight.team2.lower())