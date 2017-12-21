from fb_highlights.models import Team


def get_teams_for_user(fb_id):
    teams = Team.objects.filter(user_id=fb_id)
    return [team.team_name for team in teams]


def get_users_for_team(team):
    teams = Team.objects.filter(team_name=team)
    return [team.user.facebook_id for team in teams]


def add_team(fb_id, team):
    Team.objects.update_or_create(user_id=fb_id, team_name=team.title())


def delete_team(fb_id, team):
    Team.objects.filter(user_id=fb_id, team_name=team).delete()
