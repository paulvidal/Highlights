from datetime import datetime, timedelta

import dateparser

from fb_bot import messenger_manager
from fb_bot.highlight_fetchers import fetcher_footyroom, fetcher_hoofoot, ressource_checker, fetcher_footyroom_videos
from fb_bot.logger import logger
from fb_bot.model_managers import latest_highlight_manager, context_manager, highlight_notification_stat_manager, \
    registration_team_manager, registration_competition_manager
from fb_bot.video_providers import video_info_fetcher


# Send highlights
def send_most_recent_highlights(footyroom_pagelet=1,
                                hoofoot_pagelet=4,
                                footyroom_videos_pagelet=3):

    # Footyroom + Hoofoot highlights fetching
    highlights = fetcher_footyroom.fetch_highlights(num_pagelet=footyroom_pagelet, max_days_ago=2) \
                 + fetcher_hoofoot.fetch_highlights(num_pagelet=hoofoot_pagelet, max_days_ago=7) \
                 + fetcher_footyroom_videos.fetch_highlights(num_pagelet=footyroom_videos_pagelet, max_days_ago=7)

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

        # Add time to make sure video is good
        if timedelta(minutes=30) < abs(today - time_since_added):

            if highlight.sent:
                # highlight has already been sent
                continue

            # Log highlights sent
            logger.log("Highlight sent: " + highlight.get_match_name(), forward=True)

            # Set highlights for same match to sent
            similar_highlights = latest_highlight_manager.get_similar_highlights(highlight, not_sent_highlights)

            for h in similar_highlights:
                latest_highlight_manager.set_sent(h)

            # Send highlight to users
            _send_highlight_to_users(highlight)

    # Delete old highlights
    # FIXME: try to find a way to keep old highlights
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
            latest_highlight_manager.set_invalid(h)


# Check scrapping status of websites

def check_scrapping_status():

    # Define scrapping exception
    class ScrappingException(Exception):
        pass

    scrapping_problems = []

    highlights_footyroom = fetcher_footyroom.fetch_highlights(num_pagelet=1, max_days_ago=1000)

    if not highlights_footyroom:
        scrapping_problems.append('FOOTYROOM')

    highlights_hoofoot = fetcher_hoofoot.fetch_highlights(num_pagelet=1, max_days_ago=1000)

    if not highlights_hoofoot:
        scrapping_problems.append('HOOFOOT')

    if scrapping_problems:
        raise ScrappingException("Failed to scrape " + ', '.join(scrapping_problems))


# Add the video info such as duration

def add_videos_info():
    highlights = latest_highlight_manager.get_all_highlights_without_info()

    for h in highlights:
        info = video_info_fetcher.get_info(h.link)

        if not info:
            latest_highlight_manager.set_video_duration(h, -1)
            continue

        video_duration = info.get('duration')
        video_url = info.get('video_url')

        if video_duration:
            latest_highlight_manager.set_video_duration(h, video_duration)

        if video_url:
            latest_highlight_manager.set_video_url(h, video_url)


# HELPERS

def _send_highlight_to_users(highlight):
    team1 = highlight.team1.name.lower()
    team2 = highlight.team2.name.lower()
    competition = highlight.category.name.lower()

    user_id_team1 = registration_team_manager.get_users_for_team(team1)
    user_id_team2 = registration_team_manager.get_users_for_team(team2)
    user_id_competition = registration_competition_manager.get_users_for_competition(competition)

    ids = user_id_team1 + user_id_team2 + user_id_competition
    ids = list(set(ids)) # clear duplicates

    win_ids = []
    draw_ids = []
    lose_ids = []

    if highlight.score1 > highlight.score2:
        win_ids = [id for id in ids if id in user_id_team1 or user_id_competition]
        lose_ids = [id for id in ids if id in user_id_team2 and id not in user_id_team1 and id not in user_id_competition]

    elif highlight.score2 > highlight.score1:
        win_ids = [id for id in ids if id in user_id_team2 or user_id_competition]
        lose_ids = [id for id in ids if id in user_id_team1 and id not in user_id_team2 and id not in user_id_competition]

    else:
        win_ids = [id for id in ids if id in user_id_competition]
        draw_ids = [id for id in ids if id in (user_id_team1 or user_id_team2) and id not in user_id_competition]

    # Send introduction message to users
    messenger_manager.send_highlight_won_introduction_message(win_ids, highlight)
    messenger_manager.send_highlight_draw_introduction_message(draw_ids, highlight)
    messenger_manager.send_highlight_lost_introduction_message(lose_ids, highlight)

    # Send the highlight to users
    messenger_manager.send_highlight_messages(ids, [highlight])

    # TODO: do batch update on database
    for user_id in ids:
        # Track highlight notification
        highlight_notification_stat_manager.add_notification_stat(user_id, highlight)

        # Reset to default context
        context_manager.set_default_context(user_id)
