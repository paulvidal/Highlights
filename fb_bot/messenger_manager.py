import json
from urllib.parse import quote

import requests

import highlights.settings
import highlights.settings
from fb_bot.messages import NO_MATCH_FOUND, ERROR_MESSAGE, GET_STARTED_MESSAGE, NOTIFICATION_MESSAGE, \
    ADD_TEAM_MESSAGE, DELETE_TEAM_MESSAGE, TEAM_ADDED_SUCCESS_MESSAGE, TEAM_ADDED_FAIL_MESSAGE, TEAM_DELETED_MESSAGE, \
    HELP_MESSAGE, TEAM_NOT_FOUND_MESSAGE, TEAM_RECOMMEND_MESSAGE, DELETE_TEAM_NOT_FOUND_MESSAGE, CANCEL_MESSAGE, \
    NO_MATCH_FOUND_TEAM_RECOMMENDATION, SEARCH_HIGHLIGHTS_MESSAGE, DONE_MESSAGE, EMOJI_MAGNIFYING_GLASS, \
    EMOJI_NOTIFICATION, EMOJI_CROSS, EMOJI_DONE, EMOJI_REMOVE, EMOJI_ADD, WHAT_DO_YOU_WANT_TODO_MESSAGE, EMOJI_HELP, \
    GET_STARTED_MESSAGE_2, ANYTHING_ELSE_I_CAN_DO_MESSAGE
from fb_bot.model_managers import latest_highlight_manager, football_team_manager
from highlights import settings

ACCESS_TOKEN = highlights.settings.get_env_var('MESSENGER_ACCESS_TOKEN')

MAX_QUICK_REPLIES = 10


### MESSAGES ###

def send_help_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(HELP_MESSAGE, [EMOJI_MAGNIFYING_GLASS + ' Search highlights',
                                                                                       EMOJI_NOTIFICATION + ' Notifications']))


def send_what_do_you_want_to_do_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(WHAT_DO_YOU_WANT_TODO_MESSAGE,
                                                                        [EMOJI_MAGNIFYING_GLASS + ' Search highlights',
                                                                         EMOJI_NOTIFICATION + ' Notifications',
                                                                         EMOJI_HELP + ' Help']))


def send_anything_else_i_can_do_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(ANYTHING_ELSE_I_CAN_DO_MESSAGE,
                                                                        [EMOJI_MAGNIFYING_GLASS + ' Search highlights',
                                                                         EMOJI_NOTIFICATION + ' Notifications',
                                                                         EMOJI_HELP + ' Help']))


def send_cancel_message(fb_id):
    return send_facebook_message(fb_id, create_message(CANCEL_MESSAGE))


def send_done_message(fb_id):
    return send_facebook_message(fb_id, create_message(DONE_MESSAGE))


def send_search_highlights_message(fb_id):
    return send_facebook_message(fb_id, create_message(SEARCH_HIGHLIGHTS_MESSAGE))


def send_notification_message(fb_id, teams):
    formatted_teams = ""
    quick_reply_buttons = [EMOJI_ADD + " Add", EMOJI_REMOVE + " Remove", EMOJI_DONE + " Done"]

    if len(teams) == 0:
        formatted_teams = "-> No team registered"
        quick_reply_buttons.remove(EMOJI_REMOVE + " Remove")
    elif len(teams) == MAX_QUICK_REPLIES:
        quick_reply_buttons.remove(EMOJI_ADD + " Add")

    for i in range(len(teams)):
        if i > 0:
            formatted_teams += "\n"

        formatted_teams += "-> {}".format(teams[i])

    return send_facebook_message(
        fb_id, create_quick_text_reply_message(NOTIFICATION_MESSAGE.format(formatted_teams), quick_reply_buttons))


def send_add_team_message(fb_id):
    return send_facebook_message(fb_id, create_message(ADD_TEAM_MESSAGE))


def send_delete_team_message(fb_id, teams):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_TEAM_MESSAGE, teams + [EMOJI_CROSS + ' Cancel']))


def send_recommended_team_messages(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(TEAM_RECOMMEND_MESSAGE, recommended[:9] + ['Other', EMOJI_CROSS + ' Cancel']))


def send_team_not_found_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(TEAM_NOT_FOUND_MESSAGE, ['Try again', EMOJI_CROSS + ' Cancel']))


def send_team_added_message(fb_id, success, team):
    if success:
        return send_facebook_message(fb_id, create_message(TEAM_ADDED_SUCCESS_MESSAGE.format(team)))
    else:
        return send_facebook_message(fb_id, create_message(TEAM_ADDED_FAIL_MESSAGE.format(team)))


def send_team_to_delete_not_found_message(fb_id, teams):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_TEAM_NOT_FOUND_MESSAGE, teams + [EMOJI_CROSS + ' Cancel']))


def send_team_deleted_message(fb_id, teams):
    return send_facebook_message(fb_id, create_message(TEAM_DELETED_MESSAGE.format(teams)))


def send_getting_started_message(fb_id, user_name):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE.format(user_name)))


def send_getting_started_message_2(fb_id):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE_2))


def send_error_message(fb_id):
    return send_facebook_message(fb_id, create_message(ERROR_MESSAGE))


def send_highlight_message_for_team(fb_id, team):
    return send_facebook_message(fb_id, get_highlights_for_team(fb_id, team))


# For scheduler
def send_highlight_message(fb_id, highlight_models):
    return send_facebook_message(fb_id, create_generic_attachment(highlights_to_json(fb_id, highlight_models)))


### MAIN METHOD ###

def send_facebook_message(fb_id, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps(
        {
            "recipient": {
                "id": fb_id
            },
            "message": message
        })

    if not highlights.settings.DEBUG:
        requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)

    return response_msg


def send_typing(fb_id):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps(
        {
            "recipient": {
                "id": fb_id
            },
            "sender_action": "typing_on"
        })

    if not highlights.settings.DEBUG:
        requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)


#
# Highlights getters
#

def has_highlight_for_team(team):
    highlights = latest_highlight_manager.get_highlights_for_team(team)

    if not highlights:
        similar_team_names = football_team_manager.similar_football_team_names(team)
        similar_team_names = [team_name.title() for team_name in similar_team_names]

        # Check if name of team was not properly written
        if similar_team_names:
            return False, True
        else:
            return False, False

    return True, True


def get_highlights_for_team(fb_id, team):
    highlights = latest_highlight_manager.get_highlights_for_team(team)

    # Case no highlight found for the team
    if not highlights:
        similar_team_names = football_team_manager.similar_football_team_names(team)
        similar_team_names = [team_name.title() for team_name in similar_team_names]

        # Check if name of team was not properly written
        if similar_team_names:
            return create_quick_text_reply_message(NO_MATCH_FOUND_TEAM_RECOMMENDATION, similar_team_names[:9]
                                                   + [EMOJI_HELP + ' Help', EMOJI_CROSS + ' Cancel'])
        else:
            return create_quick_text_reply_message(NO_MATCH_FOUND, [EMOJI_HELP + ' Help'])

    # Eliminate duplicates
    highlights = latest_highlight_manager.get_unique_highlights(highlights)

    # Order highlights by date and take the first 10
    highlights = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)[:10]

    return create_generic_attachment(highlights_to_json(fb_id, highlights))


#
# Highlights to json
#


def highlights_to_json(fb_id, highlight_models):
    return list(map(lambda h: highlight_to_json(fb_id, h), highlight_models))


def highlight_to_json(fb_id, highlight_model):
    return {
        "title": highlight_model.get_match_name(),
        "image_url": highlight_model.img_link,
        "subtitle": highlight_model.get_parsed_time_since_added().strftime('%d %B %Y'),
        "default_action": {
            "type": "web_url",
            "url": create_tracking_link(fb_id, highlight_model),
            "messenger_extensions": "false",
            "webview_height_ratio": "full"
        }
    }


# Essential method for link creation and redirection to website (and tracking)
def create_tracking_link(fb_id, highlight_model):
    # Form correct url to redirect to server
    link = settings.BASE_URL + "/highlight?team1={}&score1={}&team2={}&score2={}&date={}&user_id=".format(
        quote(highlight_model.team1.name.lower()),
        highlight_model.score1,
        quote(highlight_model.team2.name.lower()),
        highlight_model.score2,
        highlight_model.get_parsed_time_since_added().date()
    )

    tracking_link = link + str(fb_id)

    return tracking_link


#
# JSON message formatter
#

def create_message(text):
    return {
        "text": text
    }


def create_quick_text_reply_message(text, quick_replies):
    formatted_quick_replies = []

    for quick_reply in quick_replies:
        formatted_quick_replies.append({
            "content_type": "text",
            "title": quick_reply,
            "payload": "NO_PAYLOAD"
        })

    return {
        "text": text,
        "quick_replies": formatted_quick_replies
    }


def create_list_attachement(elements):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "list",
                "top_element_style": "compact",
                "elements": elements
            }
        }
    }


def create_generic_attachment(elements):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
