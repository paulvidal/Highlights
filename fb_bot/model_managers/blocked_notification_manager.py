from django.db.models import Q

from fb_bot.model_managers import football_team_manager, football_competition_manager
from fb_highlights.models import BlockedNotification


def add_blocked_competition_highlight(team=None, competition=None):
    if team:
        team = football_team_manager.get_football_team(team)

    if competition:
        competition = football_competition_manager.get_football_competition(competition)

    BlockedNotification.objects.update_or_create(team=team,
                                                 competition=competition)


def is_highlight_for_competition_blocked(highlight_model):
    blocked_notifications = BlockedNotification.objects.all()

    for blocked in blocked_notifications:
        if blocked.team is None and blocked.competition == highlight_model.category:
                return True

        elif blocked.competition is None and blocked.team in [highlight_model.team1, highlight_model.team2]:
                return True

        elif blocked.team in [highlight_model.team1, highlight_model.team2] \
                and blocked.competition == highlight_model.category:
                return True

    return False
