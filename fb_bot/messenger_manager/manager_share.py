from fb_bot.messages import SHARE_INTRODUCTION_MESSAGE, EMOJI_HEART
from fb_bot.messenger_manager.formatter import create_message, create_generic_attachment
from fb_bot.messenger_manager.sender import send_facebook_message
from highlights import settings


def send_share_introduction_message(fb_id):
    return send_facebook_message(fb_id, create_message(SHARE_INTRODUCTION_MESSAGE))


def send_share_message(fb_id):
    return send_facebook_message(fb_id, create_share_message())


def create_share_message():
    return create_generic_attachment([
        {
            "title": "Start a conversation with me!",
            "subtitle": "I will send you the highlight videos for your teams as soon as matches occur.",
            "image_url": settings.BASE_URL + "/static/images/share.png",
            "buttons": [
                {
                    "type": "element_share",
                    "share_contents": create_generic_attachment([
                        {
                            "title": "Start a conversation with me!",
                            "subtitle": "I will send you the highlight videos for your teams as soon as matches occur.",
                            "image_url": settings.BASE_URL + "/static/images/share.png",
                            "default_action": {
                                "type": "web_url",
                                "url": "https://m.me/highlightsSportBot/"
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": "https://m.me/highlightsSportBot/",
                                    "title": "Start " + EMOJI_HEART
                                }
                            ]
                        }
                    ])
                }
            ]
        }
    ])