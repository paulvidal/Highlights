from datetime import datetime, timedelta

from fb_bot.model_managers import user_manager, football_team_manager
from fb_highlights.models import HighlightNotificationStat


def add_notification_stat(fb_id, highlight):
    user = user_manager.get_user(fb_id)
    send_time = datetime.now()
    match_time = highlight.get_parsed_time_since_added()

    team1 = football_team_manager.get_football_team(highlight.team1)
    team2 = football_team_manager.get_football_team(highlight.team2)

    HighlightNotificationStat.objects.update_or_create(user=user,
                                                       team1=team1,
                                                       score1=highlight.score1,
                                                       team2=team2,
                                                       score2=highlight.score2,
                                                       match_time=str(match_time),
                                                       send_time=str(send_time))


def update_notification_opened(fb_id, highlight_model):
    user = user_manager.get_user(fb_id)
    open_time = datetime.now()
    match_time = highlight_model.get_parsed_time_since_added()

    highlight_stats = HighlightNotificationStat.objects.filter(user=user,
                                                               team1=highlight_model.team1,
                                                               score1=highlight_model.score1,
                                                               team2=highlight_model.team2,
                                                               score2=highlight_model.score2)

    for highlight_stat in highlight_stats:
        if abs(match_time - highlight_stat.get_parsed_match_time()) > timedelta(days=2):
            continue

        if highlight_stat.opened:
            continue

        highlight_stat.opened = True
        highlight_stat.open_time = str(open_time)
        highlight_stat.link = highlight_model.link

        highlight_stat.save()


def get_all_highlight_notification_stats():
    return HighlightNotificationStat.objects.all()