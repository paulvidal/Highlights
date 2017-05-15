from fb_highlights.models import Team, User


def get_teams_for_user(fb_id):
    teams = Team.objects.filter(user_id=fb_id)
    return [team.team_name for team in teams]


def add_team(fb_id, team):
    Team.objects.create(user_id=fb_id, team_name=team)


def delete_team(fb_id, team):
    Team.objects.filter(user_id=fb_id, team_name=team).delete()
