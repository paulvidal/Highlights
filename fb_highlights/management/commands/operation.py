from fb_bot.highlight_fetchers.utils import mapping_football_team, mapping_football_competition
from fb_bot.model_managers import football_team_manager, football_competition_manager
from fb_highlights.management.commands.CustomCommand import CustomCommand
from fb_highlights.models import FootballTeamMapping, FootballCompetitionMapping


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'operation'

    def run_task(self, options):
        for n in mapping_football_team.NAME_MAPPING:
            name = mapping_football_team.NAME_MAPPING[n]

            try:
                team = football_team_manager.get_football_team(name)
                FootballTeamMapping.objects.update_or_create(team_name=n,
                                                             team=team)

                # print(n, team)

            except IndexError:
                print('Error with team: ' + str(n))

        for n in mapping_football_competition.NAME_MAPPING:
            name = mapping_football_competition.NAME_MAPPING[n]

            try:
                competition = football_competition_manager.get_football_competition(name)
                FootballCompetitionMapping.objects.update_or_create(competition_name=n,
                                                                    competition=competition)

                # print(n, competition)

            except IndexError:
                print('Error with competition: ' + str(n))