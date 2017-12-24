from fb_bot.model_managers import football_team_manager
from fb_highlights.models import Team


def get_teams_for_user(fb_id):
    teams = Team.objects.filter(user_id=fb_id)
    return [team.team_name.name for team in teams]


def get_users_for_team(team_name):
    team = football_team_manager.get_football_team(team_name)
    teams = Team.objects.filter(team_name=team)
    return [team.user.facebook_id for team in teams]


def add_team(fb_id, team_name):
    team = football_team_manager.get_football_team(team_name)
    Team.objects.update_or_create(user_id=fb_id, team_name=team)


def delete_team(fb_id, team_name):
    team = football_team_manager.get_football_team(team_name)
    Team.objects.filter(user_id=fb_id, team_name=team).delete()
