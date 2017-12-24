from datetime import datetime, timedelta

import dateparser

from fb_bot import highlights_fetcher
from fb_bot import messenger_manager
from fb_bot.model_managers import latest_highlight_manager
from fb_bot.model_managers import team_manager


def send_most_recent_highlights():
    most_recent_highlights = []
    highlights = highlights_fetcher.fetch_highlights(num_pagelet=2, max_days_ago=1)

    for highlight in highlights:
        link = highlight.link
        # Parse the date before inserting it (date needs to be a string)
        time_since_added = str(dateparser.parse(highlight.time_since_added))

        if not latest_highlight_manager.already_has_highlight(link):
            most_recent_highlights.append(highlight)
            latest_highlight_manager.add_highlight(link=link, time_since_added=time_since_added)

    _delete_old_highlights()

    for recent_highlight in most_recent_highlights:
        user_ids = []

        team1 = recent_highlight.team1.lower()
        user_ids += team_manager.get_users_for_team(team1)

        team2 = recent_highlight.team2.lower()
        user_ids += team_manager.get_users_for_team(team2)

        for user_id in user_ids:
            messenger_manager.send_highlight_message(user_id, recent_highlight)


def _delete_old_highlights():
    all_highlights = latest_highlight_manager.get_all_highlights()

    for highlight in all_highlights:
        today = datetime.today()
        time_since_added = dateparser.parse(highlight.time_since_added)

        if (today - time_since_added) > timedelta(days=2):
            latest_highlight_manager.delete_highlight(link=highlight.link, time_since_added=highlight.time_since_added)


if __name__ == '__main__':
    send_most_recent_highlights()