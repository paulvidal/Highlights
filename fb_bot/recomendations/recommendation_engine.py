from datetime import timedelta, datetime

from django.db.models import Q, Min, Sum

from fb_highlights.models import LatestHighlight


def get_recommendations(highlight_model):
    """
    Always returned 2 recommendations
    """

    # most vued video in past 1 week
    return LatestHighlight.objects \
        .filter(
            Q(time_since_added__gt=datetime.today() - timedelta(hours=168)) &
            ~Q(id=highlight_model.id)
        ) \
        .values('id', 'match_time', 'team1', 'score1', 'team2', 'score2', 'category') \
        .annotate(img_link=Min('img_link'), view_count=Sum('click_count')) \
        .order_by('-match_time', '-view_count')[:2]