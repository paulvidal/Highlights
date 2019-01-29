from datetime import timedelta, datetime

from django.db.models import Q, Min, Sum

from fb_bot.model_managers import highlight_stat_manager
from fb_highlights.models import LatestHighlight


def get_recommendations(highlight_model, user_id):
    """
    Always returned 2 recommendations
    """
    highlights_id = []

    if user_id != 0:
        highlights_id = highlight_stat_manager.get_highlight_stats_id_for_user(user_id)

    # most vued video in past 1 week
    return LatestHighlight.objects \
        .filter(
            Q(time_since_added__gt=datetime.today() - timedelta(hours=168)) &
            ~Q(id=highlight_model.id) &
            ~Q(id__in=highlights_id)
        ) \
        .values('id', 'match_time', 'team1', 'score1', 'team2', 'score2', 'category') \
        .annotate(img_link=Min('img_link'), view_count=Sum('click_count')) \
        .order_by('-view_count', '-match_time')[:2]