from datetime import datetime, timedelta

import dateparser

from fb_bot.model_managers import highlight_stat_manager, highlight_notification_stat_manager


def get_highlight_analytics():
    highlight_stats = highlight_stat_manager.get_all_highlight_stats()
    highlight_notification_stats = highlight_notification_stat_manager.get_all_highlight_notification_stats()

    # stats
    notification_opened_today = sum([h.opened and
                                     abs(dateparser.parse(h.open_time) - datetime.today()) <= timedelta(hours=24) and
                                     abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(hours=24)
                                     for h in highlight_notification_stats])
    notification_today_total = sum([abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(hours=24)
                                    for h in highlight_notification_stats])

    notification_opened_yesterday = sum([h.opened and
                                         abs(dateparser.parse(h.open_time) - datetime.today()) <= timedelta(hours=48) and
                                         abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(hours=48) and
                                         abs(dateparser.parse(h.open_time) - datetime.today()) >= timedelta(hours=24) and
                                         abs(dateparser.parse(h.send_time) - datetime.today()) >= timedelta(hours=24)
                                         for h in highlight_notification_stats])
    notification_yesterday_total = sum([abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(hours=48) and
                                        abs(dateparser.parse(h.send_time) - datetime.today()) >= timedelta(hours=24)
                                        for h in highlight_notification_stats])

    notification_opened_week = sum([h.opened and
                                    abs(dateparser.parse(h.open_time) - datetime.today()) <= timedelta(days=7) and
                                    abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(days=7)
                                    for h in highlight_notification_stats])
    notification_week_total = sum([abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(days=7)
                                   for h in highlight_notification_stats])

    notification_opened_month = sum([h.opened and
                                     abs(dateparser.parse(h.open_time) - datetime.today()) <= timedelta(days=30) and
                                     abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(days=30)
                                     for h in highlight_notification_stats])
    notification_month_total = sum([abs(dateparser.parse(h.send_time) - datetime.today()) <= timedelta(days=30)
                                    for h in highlight_notification_stats])

    return {
        'today_click': sum([datetime.today().date() == dateparser.parse(h.time).date() for h in highlight_stats]),
        'yesterday_click': sum([(datetime.today() - timedelta(days=1)).date() == dateparser.parse(h.time).date() for h in highlight_stats]),
        'week_click': sum([abs(dateparser.parse(h.time) - datetime.today()) <= timedelta(days=7) for h in highlight_stats]),
        'month_click': sum([abs(dateparser.parse(h.time) - datetime.today()) <= timedelta(days=30) for h in highlight_stats]),
        'notification_opened_today_ratio': round(notification_opened_today / float(notification_today_total) * 100) if notification_today_total != 0 else 0,
        'notification_opened_today': notification_opened_today,
        'notification_today_total': notification_today_total,
        'notification_opened_yesterday_ratio': round(notification_opened_yesterday / float(notification_yesterday_total) * 100) if notification_yesterday_total != 0 else 0,
        'notification_opened_yesterday': notification_opened_yesterday,
        'notification_yesterday_total': notification_yesterday_total,
        'notification_opened_week_ratio': round(notification_opened_week / float(notification_week_total) * 100) if notification_week_total != 0 else 0,
        'notification_opened_week': notification_opened_week,
        'notification_week_total': notification_week_total,
        'notification_opened_month_ratio': round(notification_opened_month / float(notification_month_total) * 100) if notification_month_total != 0 else 0,
        'notification_opened_month': notification_opened_month,
        'notification_month_total': notification_month_total,
    }