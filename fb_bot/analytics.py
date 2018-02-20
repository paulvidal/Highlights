from datetime import datetime, timedelta

from fb_highlights.models import HighlightStat, HighlightNotificationStat, User


def get_highlight_analytics():
    return {
        'total_user': get_total_user(),
        'new_users_today': get_new_users_today(),
        'new_users_yesterday': get_new_users_yesterday(),
        'total_user_with_one_highlight_click': total_user_with_one_highlight_click(),
        'today_click': get_today_click(),
        'yesterday_click': get_yesterday_click(),
        'week_click': get_week_click(),
        'month_click': get_month_click(),
        'notification_opened_today_ratio': _ratio(get_notification_opened_today, get_notification_today_total),
        'notification_opened_today': get_notification_opened_today(),
        'notification_today_total': get_notification_today_total(),
        'notification_opened_yesterday_ratio': _ratio(get_notification_opened_yesterday, get_notification_yesterday_total),
        'notification_opened_yesterday': get_notification_opened_yesterday(),
        'notification_yesterday_total': get_notification_yesterday_total(),
        'notification_opened_week_ratio': _ratio(get_notification_opened_week, get_notification_week_total),
        'notification_opened_week': get_notification_opened_week(),
        'notification_week_total': get_notification_week_total(),
        'notification_opened_month_ratio': _ratio(get_notification_opened_month, get_notification_month_total),
        'notification_opened_month': get_notification_opened_month(),
        'notification_month_total': get_notification_month_total(),
    }


def get_total_user():
    return len(User.objects.all())


def get_new_users_today():
    return len(User.objects.filter(
        join_date__contains=datetime.today().date()
    ))


def get_new_users_yesterday():
    return len(User.objects.filter(
        join_date__contains=(datetime.today() - timedelta(days=1)).date()
    ))


def total_user_with_one_highlight_click():
    return len(User.objects.filter(
        highlights_click_count__gte=1
    ))


def get_today_click():
    return len(HighlightStat.objects.filter(
        time__contains=datetime.today().date()
    ))


def get_yesterday_click():
    return len(HighlightStat.objects.filter(
        time__contains=(datetime.today() - timedelta(days=1)).date()
    ))


def get_week_click():
    return len(HighlightStat.objects.filter(
        time__gt=datetime.today() - timedelta(days=7)
    ))


def get_month_click():
    return len(HighlightStat.objects.filter(
        time__gt=datetime.today() - timedelta(days=30)
    ))


def get_notification_opened_today():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=1),
        open_time__gt=datetime.today() - timedelta(days=1),
        opened=True
    ))


def get_notification_today_total():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=1)
    ))


def get_notification_opened_yesterday():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=2),
        send_time__lt=datetime.today() - timedelta(days=1),
        open_time__gt=datetime.today() - timedelta(days=2),
        open_time__lt=datetime.today() - timedelta(days=1),
        opened=True
    ))


def get_notification_yesterday_total():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=2),
        send_time__lt=datetime.today() - timedelta(days=1),
    ))


def get_notification_opened_week():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=7),
        open_time__gt=datetime.today() - timedelta(days=7),
        opened=True
    ))


def get_notification_week_total():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=7)
    ))


def get_notification_opened_month():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=30),
        open_time__gt=datetime.today() - timedelta(days=30),
        opened=True
    ))


def get_notification_month_total():
    return len(HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=30)
    ))


def _ratio(nominator, denominator):
    return round(nominator() / float(denominator()) * 100) if denominator() != 0 else 0