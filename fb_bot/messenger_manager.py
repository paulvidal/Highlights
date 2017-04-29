import json
import requests

from fb_bot import highlights_fetcher

ACCESS_TOKEN = 'EAAJvTnLYbnkBANP32ZCoDdyBw2nMvZAQ9vkHORylXFouyhvvv4VJ65DUPncr0RpeDZCzDtCb1FUoNFA9Ayq8STkMLXMKtAVIY0Udg3EZCzNtc6BcFdcvMzZCZC7ZBHBvZCZCZC1a1QRwgKfAMorFdHcoeqa5YphsvKXFdOZBggUCHFAIgZDZD'


def send_highlight_message(fb_id, received_message):
    send_facebook_message(fb_id, _get_highlights(received_message.lower() == 'recent'))


def send_facebook_message(fb_id, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({"recipient":
                                   {"id": fb_id},
                               "message": message
                               })

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)

    print("Message sent: " + str(status.json()))


def _get_highlights(recent=False):
    return {"attachment": {
        "type": "template",
        "payload": {
            "template_type": "list",
            "top_element_style": "compact",
            "elements": _get_elements(recent)
        }
    }
    }


def _get_elements(recent):
    elems = []
    highlights = highlights_fetcher.fetch_highlights()

    print("Highlight number: " + str(len(highlights)))

    if not recent:
        # Order by most popular highlight videos
        highlights.sort(key=lambda h: h.view_count, reverse=True)

    for i in range(4):
        highlight = highlights[i]

        elems.append({
            "title": highlight.match_name,
            "image_url": highlight.img_link,
            "subtitle": highlight.time_since_added,
            "default_action": {
                "type": "web_url",
                "url": highlight.link,
                "messenger_extensions": "false",
                "webview_height_ratio": "full"
            }
        })

    return json.dumps(elems)
