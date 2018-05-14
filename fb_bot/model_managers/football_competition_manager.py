from fb_bot.highlight_fetchers.utils import mapping_football_competition
from fb_highlights.models import FootballCompetition


def has_football_competition(name):
    name = mapping_football_competition.get_exact_name(name)
    return [competition for competition in FootballCompetition.objects.filter(name=name)]


def similar_football_competition_names(name):
    similar_names = mapping_football_competition.get_similar_names(name, get_all_football_competition_names())

    # remove duplicates
    return list(set(similar_names))


def get_all_football_competition_names():
    return [team.name for team in FootballCompetition.objects.all()]


def get_football_competition(name):
    return has_football_competition(name)[0]


def add_football_competition(name):
    FootballCompetition.objects.update_or_create(name=name)


def delete_football_competition(name):
    FootballCompetition.objects.filter(name=name).delete()