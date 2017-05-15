import json
import requests
import highlights.settings
import highlights.settings

from fb_bot import highlights_fetcher
from fb_bot.messages import NO_MATCH_FOUND, ERROR_MESSAGE, GET_STARTED_MESSAGE, MENU_MESSAGE, NOTIFICATION_MESSAGE, \
    ADD_TEAM_MESSAGE, DELETE_TEAM_MESSAGE, TEAM_ADDED_SUCCESS_MESSAGE, TEAM_ADDED_FAIL_MESSAGE, TEAM_DELETED_MESSAGE

ACCESS_TOKEN = highlights.settings.get_env_var('MESSENGER_ACCESS_TOKEN')


### MESSAGES ###

def send_menu_message(fb_id):
    return send_facebook_message(
        fb_id, create_quick_text_reply_message(MENU_MESSAGE, ["Latest Highlights", "Popular Highlights", "Notifications"]))


def send_notification_message(fb_id, teams):
    formatted_teams = ""
    quick_reply_buttons = ["Add", "Delete"]

    if len(teams) == 0:
        formatted_teams = "-> No team registered"
        quick_reply_buttons = ["Add"]
    elif len(teams) == 10:
        quick_reply_buttons = ["Delete"]

    for i in range(len(teams)):
        if i > 0:
            formatted_teams += "\n"

        formatted_teams += "-> {}".format(teams[i])

    return send_facebook_message(
        fb_id, create_quick_text_reply_message(NOTIFICATION_MESSAGE.format(formatted_teams), quick_reply_buttons))


def send_add_team_message(fb_id):
    return send_facebook_message(fb_id, create_message(ADD_TEAM_MESSAGE))


def send_delete_team_message(fb_id, teams):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_TEAM_MESSAGE, teams))


def send_team_added_message(fb_id, success, team):
    if success:
        return send_facebook_message(fb_id, create_message(TEAM_ADDED_SUCCESS_MESSAGE.format(team)))
    else:
        return send_facebook_message(fb_id, create_message(TEAM_ADDED_FAIL_MESSAGE.format(team)))


def send_team_deleted_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(TEAM_DELETED_MESSAGE.format(team)))


def send_getting_started_message(fb_id):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE))


def send_error_message(fb_id):
    return send_facebook_message(fb_id, create_message(ERROR_MESSAGE))


def send_highlight_message_for_team(fb_id, team):
    return send_facebook_message(fb_id, get_highlights_for_team(team))


def send_highlight_message_recent(fb_id):
    return send_facebook_message(fb_id, get_most_recent_highlights())


def send_highlight_message_popular(fb_id):
    return send_facebook_message(fb_id, get_most_popular_highlights())


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


#
# Highlights getters
#

def get_most_recent_highlights():
    highlights = highlights_fetcher.fetch_highlights()
    highlights = truncate_num_of_highlights(highlights)

    return create_generic_attachment(highlights_to_json(highlights))


def get_most_popular_highlights():
    highlights = highlights_fetcher.fetch_highlights()

    # Order by most popular highlight videos
    highlights.sort(key=lambda h: h.view_count, reverse=True)

    highlights = truncate_num_of_highlights(highlights)

    return create_generic_attachment(highlights_to_json(highlights))


def get_highlights_for_team(team):
    highlights = highlights_fetcher.fetch_highlights_for_team(team)

    if not highlights:
        return create_message(NO_MATCH_FOUND)

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


def highlights_to_json(highlights):
    return list(map(lambda h: highlight_to_json(h), highlights))


def highlight_to_json(highlight):
    return {
        "title": highlight.match_name,
        "image_url": highlight.img_link,
        "subtitle": highlight.time_since_added,
        "default_action": {
            "type": "web_url",
            "url": highlight.link,
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
