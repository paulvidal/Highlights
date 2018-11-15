from django.db.models import Q

from fb_highlights.models import DeniedForCompetitionHighlight


def is_team_for_competition_denied(highlight_model):
    denied_for_competition_highlight = DeniedForCompetitionHighlight.objects.filter(
        (
            Q(team=highlight_model.team1) |
            Q(team=highlight_model.team2)
        )
    )

    if [d for d in denied_for_competition_highlight if d.competition == highlight_model.category or not d.competition]:
        return True

    return False