from datetime import datetime

from fb_bot.model_managers import user_manager
from fb_highlights.models import HighlightStat


def add_highlight_stat(fb_id, highlight_model):
    user = user_manager.get_user(fb_id)
    time = str(datetime.today())

    HighlightStat.objects.update_or_create(user=user,
                                           team1=highlight_model.team1,
                                           score1=highlight_model.score1,
                                           team2=highlight_model.team2,
                                           score2=highlight_model.score2,
                                           link=highlight_model.link,
                                           time=time)