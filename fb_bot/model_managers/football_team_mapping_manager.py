from fb_highlights.models import FootballTeamMapping


def get_all_football_team_name_mappings():
    football_team_name_mappings = {}

    for team_mapping in FootballTeamMapping.objects.all():
        football_team_name_mappings[team_mapping.team_name] = team_mapping.team.name

    return football_team_name_mappings