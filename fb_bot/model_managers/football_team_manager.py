from fb_bot.highlight_fetchers.utils import mapping_football_team
from fb_highlights.models import FootballTeam


def has_football_team(name):
    name = mapping_football_team.get_exact_name(name)
    return [team for team in FootballTeam.objects.filter(name=name)]


def similar_football_team_names(name):
    similar_names = mapping_football_team.get_similar_names(name, get_all_football_team_names())

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