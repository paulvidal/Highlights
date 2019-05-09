from fb_highlights.models import FootballCompetitionMapping


def get_all_football_competition_name_mappings():
    football_competition_name_mappings = {}

    for competition_mapping in FootballCompetitionMapping.objects.all():
        football_competition_name_mappings[competition_mapping.competition_name] = competition_mapping.competition.name

    return football_competition_name_mappings