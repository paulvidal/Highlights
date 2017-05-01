import json
import requests

from fb_bot import highlights_fetcher

ACCESS_TOKEN = 'EAAJvTnLYbnkBANP32ZCoDdyBw2nMvZAQ9vkHORylXFouyhvvv4VJ65DUPncr0RpeDZCzDtCb1FUoNFA9Ayq8STkMLXMKtAVIY0Udg3EZCzNtc6BcFdcvMzZCZC7ZBHBvZCZCZC1a1QRwgKfAMorFdHcoeqa5YphsvKXFdOZBggUCHFAIgZDZD'


def send_highlight_message(fb_id, received_message):
    send_facebook_message(fb_id, get_highlights_for_team(received_message))


def send_facebook_message(fb_id, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps(
        {
            "recipient": {
                    "id": fb_id
                },
            "message": message
        })

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)

    print("Message sent: " + str(status.json()))


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
    return json.dumps(map(lambda h: highlight_to_json(h), highlights))


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