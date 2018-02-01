from django.core.management.base import BaseCommand

from fb_bot.highlight_fetchers import mapping_football_team
from fb_bot.model_managers import football_team_manager


class Command(BaseCommand):

    def handle(self, *args, **options):
        all_teams = football_team_manager.get_all_football_team_names()

        for team_name in all_teams:
            exact_team_name = mapping_football_team.get_exact_name(team_name)

            if not team_name == exact_team_name:
                # add team name
                football_team_manager.add_football_team(exact_team_name)

                # delete old team name
                football_team_manager.delete_football_team(team_name)
