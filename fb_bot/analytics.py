from datetime import datetime, timedelta

from django.db.models import Count
from django.db.models.functions import TruncMonth

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

        'highlight_clicks_over_months': get_highlights_clicks_over_month(),
        'new_users_over_months': get_new_users_over_months()
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


# Highlight clicks over months

def get_highlights_clicks_over_month():
    stats = []

    total_counts = HighlightStat.objects \
        .annotate(month=TruncMonth('time')) \
        .values('month') \
        .annotate(count=Count('id'))

    notification_counts = HighlightNotificationStat.objects \
        .filter(opened=True) \
        .annotate(month=TruncMonth('open_time')) \
        .values('month') \
        .annotate(count=Count('id'))

    time = datetime.today()

    for i in range(5):
        y = time.year
        m = time.month

        m_total_count = 0
        m_notification_count = 0

        for t in total_counts:
            if t['month'].year == y and t['month'].month == m:
                m_total_count = t['count']

        for t in notification_counts:
            if t['month'].year == y and t['month'].month == m:
                m_notification_count = t['count']

        stats.append([time.strftime("%B %Y"), m_total_count, m_notification_count, m_total_count - m_notification_count])

        time = time.replace(day=1) - timedelta(days=1)

    stats.reverse()

    return [['Date', 'Total', 'Notification', 'Search']] + stats


def get_new_users_over_months():
    stats = []

    new_users_counts = User.objects \
        .annotate(month=TruncMonth('join_date')) \
        .values('month') \
        .annotate(count=Count('facebook_id'))

    new_users_with_one_highlight_click = User.objects \
        .filter(highlights_click_count__gte=1) \
        .annotate(month=TruncMonth('join_date')) \
        .values('month') \
        .annotate(count=Count('facebook_id'))

    time = datetime.today()

    for i in range(5):
        y = time.year
        m = time.month

        m_new_user_count = 0
        m_new_user_count_one_highlight_click = 0

        for t in new_users_counts:
            if t['month'].year == y and t['month'].month == m:
                m_new_user_count = t['count']

        for t in new_users_with_one_highlight_click:
            if t['month'].year == y and t['month'].month == m:
                m_new_user_count_one_highlight_click = t['count']

        stats.append([time.strftime("%B %Y"), m_new_user_count, m_new_user_count_one_highlight_click, m_new_user_count - m_new_user_count_one_highlight_click])

        time = time.replace(day=1) - timedelta(days=1)

    stats.reverse()

    return [['Date', 'New users', 'New users with 1 click', 'New users without 1 click']] + stats