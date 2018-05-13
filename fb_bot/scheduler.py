from datetime import datetime, timedelta

import dateparser
import requests

from fb_bot import messenger_manager
from fb_bot.highlight_fetchers import fetcher_footyroom, fetcher_hoofoot, ressource_checker, fetcher_highlightsfootball, \
    fetcher_sportyhl, streamable_converter
from fb_bot.highlight_fetchers.fetcher_footyroom import FootyroomVideoHighlight, FootyroomHighlight
from fb_bot.logger import logger
from fb_bot.model_managers import latest_highlight_manager, context_manager, highlight_notification_stat_manager, \
    registration_team_manager, registration_competition_manager, user_manager
from fb_bot.video_providers import video_info_fetcher
from raven.contrib.django.raven_compat.models import client


# Send highlights

AVAILABLE_SOURCES=[
    'footyroom',
    'footyroom_video',
    'hoofoot',
    'highlightsfootball',
    'sportyhl',
    'bot'
]

def send_most_recent_highlights(footyroom_pagelet=3,
                                hoofoot_pagelet=4,
                                highlightsfootball_pagelet=3,
                                sportyhl_pagelet=3):

    # Fetch highlights from multiple sources
    highlights = fetcher_footyroom.fetch_highlights(num_pagelet=footyroom_pagelet, max_days_ago=7) \
                 + fetcher_hoofoot.fetch_highlights(num_pagelet=hoofoot_pagelet, max_days_ago=7) \
                 + fetcher_highlightsfootball.fetch_highlights(num_pagelet=highlightsfootball_pagelet, max_days_ago=7) \
                 + fetcher_sportyhl.fetch_highlights(num_pagelet=sportyhl_pagelet, max_days_ago=7)

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

    # Set Footyroom infos
    for h in latest_highlight_manager.get_all_highlights_from_source(sources=['hoofoot', 'sportyhl', 'highlightsfootball']):
        footyroom_highlight = latest_highlight_manager.get_same_highlight_footyroom(h)

        if not footyroom_highlight:
            continue

        latest_highlight_manager.set_img_link(h, footyroom_highlight.img_link)
        latest_highlight_manager.set_goal_data(h, footyroom_highlight.goal_data)

        # Also add game score for specific sources
        if h.source in ['sportyhl', 'highlightsfootball']:
            latest_highlight_manager.set_score(h, footyroom_highlight.score1, footyroom_highlight.score2)

    # Send highlights not already sent
    not_sent_highlights = latest_highlight_manager.get_not_sent_highlights(AVAILABLE_SOURCES)

    today = datetime.today()

    for highlight in not_sent_highlights:
        time_since_added = highlight.get_parsed_time_since_added()

        # Add time to make sure video is good
        if timedelta(minutes=30) < abs(today - time_since_added) or highlight.priority_short > 0:

            if highlight.sent:
                # highlight has already been sent
                continue

            if highlight.score1 < 0 or highlight.score2 < 0:
                # score was not set as no similar video - invalid
                latest_highlight_manager.set_invalid(highlight)
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


# Check if highlight links are still alive (not taken down) and set it to invalid if so

def check_highlight_validity():
    highlights = latest_highlight_manager.get_all_highlights()

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

    highlights_footyroom_video = [h for h in highlights_footyroom if isinstance(h, FootyroomVideoHighlight)]
    highlights_footyroom = [h for h in highlights_footyroom if isinstance(h, FootyroomHighlight)]

    if not highlights_footyroom:
        scrapping_problems.append('FOOTYROOM')

    if not highlights_footyroom_video:
        scrapping_problems.append('FOOTYROOM VIDEOS')

    highlights_hoofoot = fetcher_hoofoot.fetch_highlights(num_pagelet=1, max_days_ago=1000)

    if not highlights_hoofoot:
        scrapping_problems.append('HOOFOOT')

    highlights_highlightsfootball = fetcher_highlightsfootball.fetch_highlights(num_pagelet=1, max_days_ago=1000)

    if not highlights_highlightsfootball:
        scrapping_problems.append('HIGHLIGHTS FOOTBALL')

    highlights_sportyhl = fetcher_sportyhl.fetch_highlights(num_pagelet=1, max_days_ago=1000)

    if not highlights_sportyhl:
        scrapping_problems.append('SPORTYHL')

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


# Create streamable video from matchat.online video
def create_streamable_videos():
    highlights = latest_highlight_manager.get_recent_highlight(minutes=60)
    highlights_time_since_added = [h.time_since_added for h in highlights]

    # remove all highlight with same date, as already converted videos
    highlights = [h for h in highlights if not highlights_time_since_added.count(h.time_since_added) == 2]

    for h in highlights:
        # Create similar streamable video and replace it in the database
        if 'matchat.online' in h.link:
            streamable_link = streamable_converter.convert(h.link)

            if streamable_link:
                latest_highlight_manager.convert_highlight(h, new_link=streamable_link, new_source='bot')


# Check if streamable video is ready
def check_streamable_videos_ready():
    highlights = latest_highlight_manager.get_not_ready_highlights()

    for h in highlights:
        link = h.link.replace('/e/', '/')
        page = requests.get(link).text

        if 'Oops!' in page:
            latest_highlight_manager.delete_highlight(h)
        elif not 'Processing Video' in page:
            latest_highlight_manager.set_ready(h)


# HELPERS

def _send_highlight_to_users(highlight):
    team1 = highlight.team1.name.lower()
    team2 = highlight.team2.name.lower()
    competition = highlight.category.name.lower()

    user_ids_team1 = registration_team_manager.get_users_for_team(team1)
    user_ids_team2 = registration_team_manager.get_users_for_team(team2)
    user_ids_competition = registration_competition_manager.get_users_for_competition(competition)

    ids = user_ids_team1 + user_ids_team2 + user_ids_competition
    ids = list(set(ids)) # clear duplicates

    win_ids = []
    draw_ids = []
    lose_ids = []

    if highlight.score1 > highlight.score2:
        win_ids = list(set(user_ids_team1 + user_ids_competition))
        lose_ids = [_id for _id in user_ids_team2 if _id not in win_ids]

    elif highlight.score2 > highlight.score1:
        win_ids = list(set(user_ids_team2 + user_ids_competition))
        lose_ids = [_id for _id in user_ids_team1 if _id not in win_ids]

    else:
        win_ids = user_ids_competition
        draw_ids = [_id for _id in list(set(user_ids_team1 + user_ids_team2)) if _id not in win_ids]

    # Do not send results to users with see result disable
    user_ids_see_result_disable = user_manager.get_user_ids_see_result_setting_disabled()

    win_ids  = [_id for _id in win_ids  if _id not in user_ids_see_result_disable]
    draw_ids = [_id for _id in draw_ids if _id not in user_ids_see_result_disable]
    lose_ids = [_id for _id in lose_ids if _id not in user_ids_see_result_disable]

    user_ids_see_result = win_ids + draw_ids + lose_ids
    user_ids_see_result_disable = [_id for _id in ids if _id in user_ids_see_result_disable]

    # Send introduction message to users
    messenger_manager.send_highlight_won_introduction_message(win_ids, highlight)
    messenger_manager.send_highlight_draw_introduction_message(draw_ids, highlight)
    messenger_manager.send_highlight_lost_introduction_message(lose_ids, highlight)
    messenger_manager.send_highlight_neutral_introduction_message(user_ids_see_result_disable, highlight)

    # Send the highlight to users
    messenger_manager.send_highlight_messages(user_ids_see_result, [highlight], see_result=True)
    messenger_manager.send_highlight_messages(user_ids_see_result_disable, [highlight], see_result=False)

    # Send the score to users
    messenger_manager.send_score(user_ids_see_result, highlight)

    # TODO: do batch update on database
    for user_id in ids:
        # Track highlight notification
        highlight_notification_stat_manager.add_notification_stat(user_id, highlight)

        # Reset to default context
        context_manager.set_default_context(user_id)
