from fb_bot.messages import *
from fb_bot.messenger_manager.formatter import create_message, create_quick_text_reply_message, create_generic_attachment
from fb_bot.messenger_manager.formatter_highlights import highlights_to_json
from fb_bot.messenger_manager.sender import send_facebook_message
from fb_bot.model_managers import latest_highlight_manager, user_manager


def send_team_not_found_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(NO_MATCH_FOUND, [SEARCH_AGAIN_HIGHLIGHTS_BUTTON,
                                                                                         HELP_BUTTON,
                                                                                         CANCEL_BUTTON]))


def send_recommended_team_or_competition_message(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(NO_MATCH_FOUND_TEAM_RECOMMENDATION, recommended[:9]
                                                                        + [HELP_BUTTON,
                                                                           CANCEL_BUTTON]))


def send_no_highlight_found_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(NO_HIGHLIGHTS_MESSAGE, [SEARCH_AGAIN_HIGHLIGHTS_BUTTON,
                                                                                                HELP_BUTTON,
                                                                                                CANCEL_BUTTON]))


def send_highlights_for_team_or_competition(fb_id, team_or_competition, highlight_count=10, default_teams=[]):
    highlights = latest_highlight_manager.get_highlights_for_team(team_or_competition) + \
                 latest_highlight_manager.get_highlights_for_competition(team_or_competition)

    if highlights == []:
        # Case no highlight found for the team_or_competition

        if not default_teams:
            return send_no_highlight_found_message(fb_id)

        # as fallback, use example such as PSG, Barcelona, Real Madrid, Spain or France
        for team in default_teams:
            highlights += latest_highlight_manager.get_highlights_for_team(team)

            if highlights != []:
                break

    # Order highlights by date
    highlights = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)

    # Eliminate duplicates
    highlights = latest_highlight_manager.get_unique_highlights(highlights, max_count=highlight_count)

    # Check if user has see result activated
    see_result_setting = user_manager.get_see_result_setting(fb_id)

    return send_facebook_message(fb_id, create_generic_attachment(highlights_to_json(fb_id, highlights, see_result=see_result_setting)))


"""
FOR TUTORIAL
"""

def send_tutorial_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(TUTORIAL_MESSAGE.format(team)))


def send_recommended_team_or_competition_tutorial_message(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_RECOMMEND_MESSAGE, recommended[:10] + [OTHER_BUTTON]))


def send_team_not_found_tutorial_message(fb_id):
    return send_facebook_message(fb_id, create_message(REGISTRATION_NOT_FOUND_MESSAGE))