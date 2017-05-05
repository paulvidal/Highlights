import json
import requests
import highlights.settings
import highlights.settings

from fb_bot import highlights_fetcher

ACCESS_TOKEN = highlights.settings.get_env_var('MESSENGER_ACCESS_TOKEN')


def send_highlight_message_for_team(fb_id, team):
    return send_facebook_message(fb_id, get_highlights_for_team(team))


def send_highlight_message_recent(fb_id):
    return send_facebook_message(fb_id, get_most_recent_highlights())


def send_highlight_message_popular(fb_id):
    return send_facebook_message(fb_id, get_most_popular_highlights())


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
        return create_message("No match found for this team :(")

    highlights = truncate_num_of_highlights(highlights)

    return create_generic_attachment(highlights_to_json(highlights))


# Limit to ten highlights as facebook doesn't allow more than 10 views in generic view
def truncate_num_of_highlights(highlights):
    if len(highlights) > 10:
        highlights = highlights[:10]

    return highlights


#
# JSON formatter
#

def create_message(text):
    return {
        "text": text
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