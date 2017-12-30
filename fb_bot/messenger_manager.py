import json

import requests

import highlights.settings
import highlights.settings
from fb_bot.messages import NO_MATCH_FOUND, ERROR_MESSAGE, GET_STARTED_MESSAGE, NOTIFICATION_MESSAGE, \
    ADD_TEAM_MESSAGE, DELETE_TEAM_MESSAGE, TEAM_ADDED_SUCCESS_MESSAGE, TEAM_ADDED_FAIL_MESSAGE, TEAM_DELETED_MESSAGE, \
    HELP_MESSAGE, TEAM_NOT_FOUND_MESSAGE, TEAM_RECOMMEND_MESSAGE, DELETE_TEAM_NOT_FOUND_MESSAGE, CANCEL_MESSAGE, \
    NO_MATCH_FOUND_TEAM_RECOMMENDATION, SEARCH_HIGHLIGHTS_MESSAGE
from fb_bot.model_managers import latest_highlight_manager, football_team_manager

ACCESS_TOKEN = highlights.settings.get_env_var('MESSENGER_ACCESS_TOKEN')

MAX_QUICK_REPLIES = 10


### MESSAGES ###

def send_help_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(HELP_MESSAGE, ['Notifications', 'Search highlights', 'Cancel']))


def send_cancel_message(fb_id):
    return send_facebook_message(fb_id, create_message(CANCEL_MESSAGE))


def send_search_highlights_message(fb_id):
    return send_facebook_message(fb_id, create_message(SEARCH_HIGHLIGHTS_MESSAGE))


def send_notification_message(fb_id, teams):
    formatted_teams = ""
    quick_reply_buttons = ["Add", "Delete", "Cancel"]

    if len(teams) == 0:
        formatted_teams = "-> No team registered"
        quick_reply_buttons.remove("Delete")
    elif len(teams) == MAX_QUICK_REPLIES:
        quick_reply_buttons.remove("Add")

    for i in range(len(teams)):
        if i > 0:
            formatted_teams += "\n"

        formatted_teams += "-> {}".format(teams[i])

    return send_facebook_message(
        fb_id, create_quick_text_reply_message(NOTIFICATION_MESSAGE.format(formatted_teams), quick_reply_buttons))


def send_add_team_message(fb_id):
    return send_facebook_message(fb_id, create_message(ADD_TEAM_MESSAGE))


def send_delete_team_message(fb_id, teams):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_TEAM_MESSAGE, teams + ['Cancel']))


def send_recommended_team_messages(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(TEAM_RECOMMEND_MESSAGE, recommended + ['Other']))


def send_team_not_found_message(fb_id):
    return send_facebook_message(fb_id, TEAM_NOT_FOUND_MESSAGE)


def send_team_added_message(fb_id, success, team):
    if success:
        return send_facebook_message(fb_id, create_message(TEAM_ADDED_SUCCESS_MESSAGE.format(team)))
    else:
        return send_facebook_message(fb_id, create_message(TEAM_ADDED_FAIL_MESSAGE.format(team)))


def send_team_to_delete_not_found_message(fb_id, teams):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_TEAM_NOT_FOUND_MESSAGE, teams + ['Cancel']))


def send_team_deleted_message(fb_id, teams):
    return send_facebook_message(fb_id, create_message(TEAM_DELETED_MESSAGE.format(teams)))


def send_getting_started_message(fb_id, user_name):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE.format(user_name)))


def send_error_message(fb_id):
    return send_facebook_message(fb_id, create_message(ERROR_MESSAGE))


def send_highlight_message_for_team(fb_id, team):
    return send_facebook_message(fb_id, get_highlights_for_team(team))


# For scheduler
def send_highlight_message(fb_id, highlight_model):
    return send_facebook_message(fb_id, create_generic_attachment(highlights_to_json([highlight_model])))


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

def get_highlights_for_team(team):
    highlights = latest_highlight_manager.get_highlights_for_team(team)

    # Case no highlight found for the team
    if not highlights:
        similar_team_names = football_team_manager.similar_football_team_names(team)
        similar_team_names = [team_name.title() for team_name in similar_team_names]

        # Check if name of team was not properly written
        if similar_team_names:
            return create_quick_text_reply_message(NO_MATCH_FOUND_TEAM_RECOMMENDATION, similar_team_names[:9] + ['Help', 'Cancel'])
        else:
            return create_quick_text_reply_message(NO_MATCH_FOUND, ['Help'])

    # Order highlights by date
    highlights = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)

    highlights = truncate_num_of_highlights(highlights)

    return create_generic_attachment(highlights_to_json(highlights))


# Limit to ten highlights as facebook doesn't allow more than 10 views in generic view
def truncate_num_of_highlights(highlights):
    if len(highlights) > 10:
        highlights = highlights[:10]

    return highlights


#
# Highlights to json
#


def highlights_to_json(highlight_models):
    return list(map(lambda h: highlight_to_json(h), highlight_models))


def highlight_to_json(highlight_model):
    return {
        "title": highlight_model.get_match_name(),
        "image_url": highlight_model.img_link,
        "subtitle": highlight_model.time_since_added,
        "default_action": {
            "type": "web_url",
            "url": highlight_model.link,
            "messenger_extensions": "false",
            "webview_height_ratio": "full"
        }
    }


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
