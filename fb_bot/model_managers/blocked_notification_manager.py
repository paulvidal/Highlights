from django.db.models import Q

from fb_highlights.models import BlockedNotification


def is_highlight_for_competition_blocked(highlight_model):
    blocked_competitions = BlockedNotification.objects.filter(
        (
            Q(team=highlight_model.team1) |
            Q(team=highlight_model.team2)
        )
    )

    return [blocked for blocked in blocked_competitions if blocked.competition == highlight_model.category or not blocked.competition]