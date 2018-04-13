from django.core.management import BaseCommand

from fb_bot.highlight_fetchers import mapping_football_competition
from fb_bot.model_managers import football_competition_manager, latest_highlight_manager
from fb_highlights.models import LatestHighlight


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_highlights = latest_highlight_manager.get_all_highlights()

        for h in all_highlights:
            h.category = mapping_football_competition.get_exact_name(h.category.lower())
            h.save()

        all_competitions = list(set([h.category for h in LatestHighlight.objects.all()]))

        for competition in all_competitions:
            football_competition_manager.add_football_competition(competition)