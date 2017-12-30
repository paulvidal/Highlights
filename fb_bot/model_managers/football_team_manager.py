from fb_bot.highlight_fetchers import football_team_mapping
from fb_highlights.models import FootballTeam


def has_football_team(name):
    name = football_team_mapping.get_exact_name(name)
    return [team for team in FootballTeam.objects.filter(name=name)]


def similar_football_team_names(name):
    similar_names = [team.name for team in FootballTeam.objects.all() if team.name.startswith(name)] \
                    + football_team_mapping.get_similar_names_in_mapping(name)

    # remove duplicates
    return list(set(similar_names))


def get_all_football_team_names():
    return [team.name for team in FootballTeam.objects.all()]


def get_football_team(name):
    return has_football_team(name)[0]


def add_football_team(name):
    FootballTeam.objects.update_or_create(name=name)


def delete_football_team(name):
    FootballTeam.objects.filter(name=name).delete()