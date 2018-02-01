from datetime import datetime, timedelta

import dateparser

from fb_bot import messenger_manager
from fb_bot.highlight_fetchers import fetcher_footyroom, fetcher_hoofoot, ressource_checker, fetcher_footyroom_videos
from fb_bot.logger import logger
from fb_bot.model_managers import latest_highlight_manager, context_manager, highlight_notification_stat_manager
from fb_bot.model_managers import team_manager


# Send highlights
from fb_bot.model_managers.context_manager import ContextType


def send_most_recent_highlights():
    # Footyroom + Hoofoot highlights fetching
    highlights = fetcher_footyroom.fetch_highlights(num_pagelet=1, max_days_ago=2) \
                 + fetcher_hoofoot.fetch_highlights(num_pagelet=4, max_days_ago=7) \
                 + fetcher_footyroom_videos.fetch_highlights(num_pagelet=3, max_days_ago=7)

    # Add new highlights
    for highlight in highlights:
        # Parse the date before inserting it (date needs to be a string)
        highlight.time_since_added = str(dateparser.parse(highlight.time_since_added))

        if latest_highlight_manager.has_highlight(highlight):
            # Skip if highlight already in database
            continue

        sent = False

        # Mark as sent if a similar highlight (same match, different provider) is in database and has already been sent
        if latest_highlight_manager.get_similar_sent_highlights(highlight):
            sent = True

        latest_highlight_manager.add_highlight(highlight, sent=sent)

    # Set Footyroom images for hoofoot highlights
    for hoofoot_highlight in latest_highlight_manager.get_all_highlights_from_source(source='hoofoot'):
        img_link = latest_highlight_manager.get_highlight_img_link_from_footyroom(hoofoot_highlight)

        if not img_link:
            continue

        latest_highlight_manager.set_img_link(hoofoot_highlight, img_link)

    # Send highlights not already sent
    not_sent_highlights = latest_highlight_manager.get_not_sent_highlights()

    today = datetime.today()

    for highlight in not_sent_highlights:
        time_since_added = highlight.get_parsed_time_since_added()

        # TODO: remove time when FOOTYROOM will be parsed
        if timedelta(minutes=10) < abs(today - time_since_added):

            if highlight.sent:
                # highlight has already been sent
                continue

            # Log highlights sent
            logger.log("Highlight sent: " + highlight.get_match_name())

            # Send highlight for team1
            team1 = highlight.team1.name.lower()
            send_highlight_to_users(highlight, team1)

            # Send highlight for team2
            team2 = highlight.team2.name.lower()
            send_highlight_to_users(highlight, team2)

            # Set highlights for same match to sent
            similar_highlights = latest_highlight_manager.get_similar_highlights(highlight, not_sent_highlights)

            for h in similar_highlights:
                latest_highlight_manager.set_sent(h)

    # Delete old highlights
    all_highlights = latest_highlight_manager.get_all_highlights()

    for highlight in all_highlights:
        time_since_added = highlight.get_parsed_time_since_added()

        # Old highlight, delete
        if (today - time_since_added) > timedelta(days=60):
            latest_highlight_manager.delete_highlight(highlight)


# Check if highlight links are still alive (not taken down) and remove it if so

def check_highlight_validity():
    highlights = latest_highlight_manager.get_all_highlights_from_source(source='hoofoot') \
                 + latest_highlight_manager.get_all_highlights_from_source(source='footyroom_video')

    for h in highlights:
        is_valid = ressource_checker.check(h.link)

        if not is_valid:
            latest_highlight_manager.delete_highlight(h)


# HELPERS

def send_highlight_to_users(highlight, team):

    for user_id in team_manager.get_users_for_team(team):
        # Send introduction message to user
        messenger_manager.send_highlight_message_for_team_message(user_id, team.title())
        # Send the highlight
        messenger_manager.send_highlight_message(user_id, [highlight])

        # Track highlight notification
        highlight_notification_stat_manager.add_notification_stat(user_id, highlight)

        # Reset the context to none
        context_manager.update_context(user_id, ContextType.NONE)