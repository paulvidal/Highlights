from datetime import datetime, timedelta

from fb_bot.model_managers import user_manager
from fb_highlights.models import HighlightStat


def add_highlight_stat(fb_id, highlight_model):
    user = user_manager.get_user(fb_id)
    time = datetime.today()

    highlight_stats = HighlightStat.objects.filter(user=user,
                                                   team1=highlight_model.team1,
                                                   score1=highlight_model.score1,
                                                   team2=highlight_model.team2,
                                                   score2=highlight_model.score2,
                                                   link=highlight_model.link)

    # Do not insert 2 time the same event if there are only 5 minutes difference
    for highlight_stat in highlight_stats:
        highlight_time = highlight_stat.time

        if abs(highlight_time - time) < timedelta(minutes=5):
            return

    HighlightStat.objects.update_or_create(user=user,
                                           team1=highlight_model.team1,
                                           score1=highlight_model.score1,
                                           team2=highlight_model.team2,
                                           score2=highlight_model.score2,
                                           link=highlight_model.link,
                                           time=time)