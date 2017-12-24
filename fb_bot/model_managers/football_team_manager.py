from fb_highlights.models import FootballTeam


def has_football_team(name):
    return [team for team in FootballTeam.objects.filter(name=name)]


def similar_football_teams(name):
    return [team.name for team in FootballTeam.objects.all() if team.name.startswith(name)]


def get_football_team(name):
    return has_football_team(name)[0]


def add_football_team(name):
    FootballTeam.objects.update_or_create(name=name)


def delete_football_team(name):
    FootballTeam.objects.filter(name=name).delete()