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

        'unique_highlight_viewer_today': get_unique_highlight_viewer_today(),
        'unique_highlight_viewer_yesterday': get_unique_highlight_viewer_yesterday(),
        'unique_highlight_viewer_week': get_unique_highlight_viewer_this_week(),
        'unique_highlight_viewer_month': get_unique_highlight_viewer_this_month(),

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


# User stats

def get_total_user():
    return User.objects.all().count()


def get_new_users_today():
    return User.objects.filter(
        join_date__contains=datetime.today().date()
    ).count()


def get_new_users_yesterday():
    return User.objects.filter(
        join_date__contains=(datetime.today() - timedelta(days=1)).date()
    ).count()


def total_user_with_one_highlight_click():
    return User.objects.filter(
        highlights_click_count__gte=1
    ).count()


# Highlight click stats

def get_today_click():
    return HighlightStat.objects.filter(
        time__contains=datetime.today().date()
    ).count()


def get_yesterday_click():
    return HighlightStat.objects.filter(
        time__contains=(datetime.today() - timedelta(days=1)).date()
    ).count()


def get_week_click():
    return HighlightStat.objects.filter(
        time__gt=datetime.today() - timedelta(days=7)
    ).count()


def get_month_click():
    return HighlightStat.objects.filter(
        time__gt=datetime.today() - timedelta(days=30)
    ).count()


# Unique user highlight click stats

def get_unique_highlight_viewer_today():
    return HighlightStat.objects.filter(
        time__contains=datetime.today().date()
    ).distinct('user').count()


def get_unique_highlight_viewer_yesterday():
    return HighlightStat.objects.filter(
        time__contains=(datetime.today() - timedelta(days=1)).date()
    ).distinct('user').count()


def get_unique_highlight_viewer_this_week():
    return HighlightStat.objects.filter(
        time__gt=datetime.today() - timedelta(days=7)
    ).distinct('user').count()


def get_unique_highlight_viewer_this_month():
    return HighlightStat.objects.filter(
        time__gt=datetime.today() - timedelta(days=30)
    ).distinct('user').count()


# Notification stats

def get_notification_opened_today():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=1),
        open_time__gt=datetime.today() - timedelta(days=1),
        opened=True
    ).count()


def get_notification_today_total():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=1)
    ).count()


def get_notification_opened_yesterday():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=2),
        send_time__lt=datetime.today() - timedelta(days=1),
        open_time__gt=datetime.today() - timedelta(days=2),
        open_time__lt=datetime.today() - timedelta(days=1),
        opened=True
    ).count()


def get_notification_yesterday_total():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=2),
        send_time__lt=datetime.today() - timedelta(days=1),
    ).count()


def get_notification_opened_week():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=7),
        open_time__gt=datetime.today() - timedelta(days=7),
        opened=True
    ).count()


def get_notification_week_total():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=7)
    ).count()


def get_notification_opened_month():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=30),
        open_time__gt=datetime.today() - timedelta(days=30),
        opened=True
    ).count()


def get_notification_month_total():
    return HighlightNotificationStat.objects.filter(
        send_time__gt=datetime.today() - timedelta(days=30)
    ).count()


def _ratio(nominator, denominator):
    return round(nominator() / float(denominator()) * 100) if denominator() != 0 else 0