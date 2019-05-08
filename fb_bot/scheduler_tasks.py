from datetime import datetime, timedelta

import requests

from fb_bot.messenger_manager import manager_scheduler
from fb_bot import streamable_converter, ressource_checker
from fb_bot.highlight_fetchers import fetcher
from fb_bot.highlight_fetchers.info import sources, providers
from fb_bot.logger import logger
from fb_bot.messenger_manager.sender import CLIENT
from fb_bot.model_managers import latest_highlight_manager, context_manager, highlight_notification_stat_manager, \
    registration_team_manager, registration_competition_manager, user_manager, blocked_notification_manager
from fb_bot.model_managers.latest_highlight_manager import MIN_MINUTES_TO_SEND_HIGHLIGHTS
from fb_bot.highlight_info_fetchers import info_fetcher


AVAILABLE_SOURCES = sources.get_available_sources()


def fetch_highlights(site):
    highlights = fetcher.fetch(site)

    # Add new highlights
    for highlight in highlights:

        if latest_highlight_manager.has_highlight(highlight):
            # Skip if highlight already in database
            continue

        # Determine if highlight with teams inverted exists (Barcelona - Arsenal instead of Arsenal - Barcelona)
        inverted_highlights = latest_highlight_manager.get_inverted_teams_highlights(highlight)

        if len(inverted_highlights) > 1 or any([h.sent for h in inverted_highlights]):
            highlight.swap_home_side()

        # Mark as sent if a similar highlight (same match, different provider) is in database and has already been sent
        sent = False

        if latest_highlight_manager.get_same_highlights_sent(highlight):
            sent = True

        latest_highlight_manager.add_highlight(highlight, sent=sent)


def send_most_recent_highlights():
    # Set incomplete infos
    for h in latest_highlight_manager.get_recent_highlights_with_incomplete_infos():
        reference_highlight = latest_highlight_manager.get_same_highlight_from_sources(h, sources.get_sources_with_complete_data_in_order_of_priority())

        if not reference_highlight:
            continue

        # Do not override if default image for reference highlight
        if not latest_highlight_manager.is_default_highlight_img(reference_highlight.img_link):
            latest_highlight_manager.set_img_link(h, reference_highlight.img_link)

        latest_highlight_manager.set_goal_data(h, reference_highlight.goal_data)
        latest_highlight_manager.set_score(h, reference_highlight.score1, reference_highlight.score2)

    # Send highlights not already sent
    not_sent_highlights = latest_highlight_manager.get_valid_not_sent_highlights(AVAILABLE_SOURCES)

    time_now = datetime.now()

    for highlight in not_sent_highlights:

        if _should_send_highlight(time_now, highlight):

            # prevent sending 2 times same highlight with inverted home and away teams
            inverted_highlights = latest_highlight_manager.get_inverted_teams_highlights(highlight)

            if any([h.sent for h in inverted_highlights]):
                new_id = inverted_highlights[0].id
                latest_highlight_manager.swap_home_side(highlight, new_id)

            # prevent from sending a highlight if find the same already sent
            if latest_highlight_manager.get_same_highlights_sent(highlight):
                latest_highlight_manager.set_sent(highlight)
                continue

            # Set highlights for same match to sent
            similar_highlights = latest_highlight_manager.get_similar_highlights(highlight, not_sent_highlights)

            for h in similar_highlights:
                latest_highlight_manager.set_sent(h)

            # Log highlights sent
            logger.log("Highlight sent: " + highlight.get_match_name(), forward=True)

            # Send highlight to users
            _send_highlight_to_users(highlight)

    # Delete old highlights
    # FIXME: try to find a way to keep old highlights
    all_highlights = latest_highlight_manager.get_all_highlights()

    for highlight in all_highlights:
        time_since_added = highlight.get_parsed_time_since_added()

        # Old highlight, delete
        if (time_now - time_since_added) > timedelta(days=60):
            latest_highlight_manager.delete_highlight(highlight)


def _should_send_highlight(time_now, highlight):
    """Determine if we should send the highlight - send if ONE OF THE FOLLOWING:
    - match highlight is older than MIN_MINUTES_TO_SEND_HIGHLIGHTS and younger than 30 hours
    - match has a priority set on it
    - no goals have been scored in the last 10 minutes of the game (otherwise we might miss a goal on the highlight)

    Requirements to send:
    - not footyroom video with unknown duration (as footyroom often puts old youtube videos, which can be send)
    - not a default image if less than MIN_MINUTES_TO_SEND_HIGHLIGHTS
    """
    time_since_added = highlight.get_parsed_time_since_added()

    # TODO: bad heuristic to prevent old footyroom videos from being sent bug, TEMPORARY fix, replace when check if match existed
    return (
            timedelta(minutes=MIN_MINUTES_TO_SEND_HIGHLIGHTS) < abs(time_now - time_since_added) < timedelta(hours=30)
            or highlight.priority_short > 0
            or _has_all_goal_data(highlight)
        ) and not (
            (highlight.source == sources.FOOTYROOM and highlight.video_duration == -1)
            or (highlight.source == sources.FOOTYROOM_VIDEOS and highlight.video_duration == -1)
            or (latest_highlight_manager.is_default_highlight_img(highlight.img_link) and abs(time_now - time_since_added) < timedelta(minutes=MIN_MINUTES_TO_SEND_HIGHLIGHTS))
    )


def _has_all_goal_data(highlight):
    # If there are no goals, send the highlight
    if highlight.score1 + highlight.score2 == 0:
        return True

    # Otherwise, make sure we have goal data before sending the highlight
    goals_elapsed = highlight.get_goals_elapsed()
    return len(goals_elapsed) > 0 and not any([g > 80 for g in goals_elapsed])


# Check if highlight links are still alive (not taken down) and set it to invalid if so

def check_recent_highlight_validity():
    recent_highlights = latest_highlight_manager.get_recent_valid_highlights(hours=72)
    logger.log("Checking validity of {} recent highlights (< 72 hours)".format(len(recent_highlights)))
    _check_validity(recent_highlights)


def check_highlight_validity():
    highlights = latest_highlight_manager.get_all_valid_highlights()
    logger.log("Checking validity of {} highlights (all)".format(len(highlights)))
    _check_validity(highlights)


def _check_validity(highlights):
    for h in highlights:
        try:
            is_valid = ressource_checker.check(h.link)

            if not is_valid:
                logger.log("Invalidated highlight: " + h.link)
                latest_highlight_manager.set_invalid(h)

        except:
            print(h.link)
            logger.error("Failed to validate link: {}".format(h.link))


# Add the video info such as duration
def add_videos_info():
    highlights = latest_highlight_manager.get_all_highlights_without_info()

    logger.log('Total highlights info to add: {}'.format(len(highlights)), forward=True)

    for h in highlights:
        info = info_fetcher.get_info(h.link)

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
    highlights = latest_highlight_manager.get_recent_highlights(minutes=300)
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

    # FIXME: stop sending champions league, europa league temporary
    # if (competition == 'europa league' or competition == 'champions league') and datetime.now() < datetime(2018, 9, 1):
    #     user_ids_competition = []

    # Verify sending highlight for this team and competition has not been blocked
    if blocked_notification_manager.is_highlight_for_competition_blocked(highlight):
        user_ids_competition = []

    ids = user_ids_team1 + user_ids_team2 + user_ids_competition
    ids = list(set(ids)) # clear duplicates

    # Do not send results to users with see result disable
    user_ids_see_result_disable = user_manager.get_user_ids_see_result_setting_disabled()

    user_ids_see_result = [_id for _id in ids  if _id not in user_ids_see_result_disable]
    user_ids_see_result_disable = [_id for _id in ids if _id in user_ids_see_result_disable]

    _send_highlight(user_ids_see_result, highlight, see_result=True)
    _send_highlight(user_ids_see_result_disable, highlight, see_result=False)

    # TODO: do batch update on database
    for user_id in ids:
        # Track highlight notification
        highlight_notification_stat_manager.add_notification_stat(user_id, highlight)

        # Reset to default context
        context_manager.set_default_context(user_id)


def _send_highlight(fb_ids, highlight, see_result):

    for fb_ids_chunk in _chunks(fb_ids, 40): # choose chunks of 40
        # Send the highlight to users
        manager_scheduler.send_highlight_messages(fb_ids_chunk, [highlight], see_result=see_result)

        # Send the score to users
        if see_result:
            manager_scheduler.send_score(fb_ids_chunk, highlight)


def _chunks(l, n):
    """Yield successive n-sized chunks from list l"""
    for i in range(0, len(l), n):
        yield l[i:i + n]