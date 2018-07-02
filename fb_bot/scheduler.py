from datetime import datetime, timedelta

import dateparser
import requests

from fb_bot import messenger_manager, streamable_converter, ressource_checker
from fb_bot.highlight_fetchers import fetcher
from fb_bot.highlight_fetchers.info import sources, providers
from fb_bot.logger import logger
from fb_bot.model_managers import latest_highlight_manager, context_manager, highlight_notification_stat_manager, \
    registration_team_manager, registration_competition_manager, user_manager
from fb_bot.video_providers import video_info_fetcher

# Send highlights

AVAILABLE_SOURCES = sources.get_available_sources()


def send_most_recent_highlights(fetch=True):
    highlights = []

    # Fetch highlights from multiple sources
    if fetch:
        highlights += fetcher.fetch_all_highlights()

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

    # Set incomplete infos
    for h in latest_highlight_manager.get_all_highlights_from_source(sources=sources.get_sources_with_incomplete_data()):
        if h.goal_data and h.score1 and h.score2 and h.img_link:
            continue

        reference_highlight = latest_highlight_manager.get_same_highlight_from_sources(h, sources.get_sources_with_complete_data_in_order_of_priority())

        if not reference_highlight:
            continue

        # Do not override if default image
        if not 'nothumb' in reference_highlight.img_link and not 'default' in reference_highlight.img_link:
            latest_highlight_manager.set_img_link(h, reference_highlight.img_link)

        latest_highlight_manager.set_goal_data(h, reference_highlight.goal_data)
        latest_highlight_manager.set_score(h, reference_highlight.score1, reference_highlight.score2)

    # Send highlights not already sent
    not_sent_highlights = latest_highlight_manager.get_valid_not_sent_highlights(AVAILABLE_SOURCES)

    today = datetime.today()

    for highlight in not_sent_highlights:
        time_since_added = highlight.get_parsed_time_since_added()

        # Add time to make sure video is good
        if timedelta(minutes=30) < abs(today - time_since_added) or highlight.priority_short > 0:

            if latest_highlight_manager.get_similar_sent_highlights(highlight):
                # prevent from sending a highlight if find any similar already sent
                latest_highlight_manager.set_sent(highlight)
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

    scrapping_problems = fetcher.get_fetching_status()

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

            if video_duration > 600:
                # Mark a video of more than 10 minutes extended
                latest_highlight_manager.set_extended_type(h)

        if video_url:
            latest_highlight_manager.set_video_url(h, video_url)


# Create streamable video from matchat.online video
def create_streamable_videos():
    highlights = latest_highlight_manager.get_recent_highlight(minutes=300)
    highlights_time_since_added = [h.time_since_added for h in highlights]

    # remove all highlight with same date, as already converted videos
    highlights = [h for h in highlights if (not highlights_time_since_added.count(h.time_since_added) >= 2)
                                            and providers.MATCHAT_ONLINE in h.link]

    for h in highlights:
        # Create similar 2 similar streamable videos and replace it in the database
        streamable_link = streamable_converter.convert(h.link)
        streamable_link_2 = streamable_converter.convert(h.link)

        if streamable_link:
            latest_highlight_manager.convert_highlight(h, new_link=streamable_link, new_source=sources.BOT)
        if streamable_link_2:
            latest_highlight_manager.convert_highlight(h, new_link=streamable_link_2, new_source=sources.BOT)


# Check if streamable video is ready
def check_streamable_videos_ready():
    highlights = latest_highlight_manager.get_not_ready_highlights()

    for h in highlights:
        link = h.link.replace('/e/', '/')
        page = requests.get(link).text

        if 'Oops!' in page:
            latest_highlight_manager.delete_highlight(h)
        elif not 'Processing Video' in page:
            # latest_highlight_manager.set_ready(h)
            pass


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

    user_ids_see_result_disable = [_id for _id in ids if _id in user_ids_see_result_disable]

    send_highlight(win_ids, highlight, messenger_manager.send_highlight_won_introduction_message, see_result=True)
    send_highlight(draw_ids, highlight, messenger_manager.send_highlight_draw_introduction_message, see_result=True)
    send_highlight(lose_ids, highlight, messenger_manager.send_highlight_lost_introduction_message, see_result=True)

    send_highlight(user_ids_see_result_disable, highlight, messenger_manager.send_highlight_neutral_introduction_message, see_result=False)

    # TODO: do batch update on database
    for user_id in ids:
        # Track highlight notification
        highlight_notification_stat_manager.add_notification_stat(user_id, highlight)

        # Reset to default context
        context_manager.set_default_context(user_id)


def send_highlight(fb_ids, highlight, send_intro_message_f, see_result):

    for fb_ids_chunk in chunks(fb_ids, 40): # choose chunks of 40

        # Send introduction message to users
        send_intro_message_f(fb_ids_chunk, highlight)

        # Send the highlight to users
        messenger_manager.send_highlight_messages(fb_ids_chunk, [highlight], see_result=see_result)

        # Send the score to users
        if see_result:
            messenger_manager.send_score(fb_ids_chunk, highlight)


def chunks(l, n):
    """Yield successive n-sized chunks from list l"""
    for i in range(0, len(l), n):
        yield l[i:i + n]