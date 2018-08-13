import json

import highlights.settings
from fb_bot import client
from fb_bot.logger import logger
from highlights import settings

CLIENT = client.Client()

GRAPH_VERSION = 'v2.12'
ACCESS_TOKEN = highlights.settings.get_env_var('MESSENGER_ACCESS_TOKEN')

GRAPH_URL = 'https://graph.facebook.com/{}/me/messages?access_token={}'.format(GRAPH_VERSION, ACCESS_TOKEN)


def send_batch_multiple_facebook_messages(fb_ids, messages):
    """
    Send multiple messages to all fb_id (2 or more message in a row to the same user)
    Does this in a chunk manner so people get the message at the same time in order
    """
    response_msgs = []
    messages_to_send = []

    def chunks(l, n):
        """Yield successive n-sized chunks from list l"""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    for fb_ids_chunk in chunks(fb_ids, 50): # choose chunks of 50

        for message in messages:

            for fb_id in fb_ids_chunk:

                fb_message = json.dumps(
                    {
                        "recipient": {
                            "id": str(fb_id)
                        },
                        "messaging_type": "MESSAGE_TAG",  # Messaging type is MESSAGE_TAG, NON_PROMOTIONAL_SUBSCRIPTION
                        "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
                        "message": message
                    })

                messages_to_send.append(fb_message)
                response_msgs.append(fb_message)

            CLIENT.send_fb_messages_async(GRAPH_URL, messages_to_send)
            messages_to_send = []

    if not settings.is_prod():
        logger.log(response_msgs)

    return response_msgs


def send_batch_different_facebook_messages(fb_ids, messages):
    """
    Send different messages to all fb_id
    """
    response_msgs = []

    for i in range(len(fb_ids)):
        response_msgs.append(json.dumps(
            {
                "recipient": {
                    "id": str(fb_ids[i])
                },
                "messaging_type": "MESSAGE_TAG",  # Messaging type is MESSAGE_TAG, NON_PROMOTIONAL_SUBSCRIPTION
                "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
                "message": messages[i]
            })
        )

    CLIENT.send_fb_messages_async(GRAPH_URL, response_msgs)

    if not settings.is_prod():
        logger.log(response_msgs)

    return response_msgs


def send_batch_facebook_message(fb_ids, message):
    """
    Send same message to all fb_id
    """
    response_msgs = []

    for i in range(len(fb_ids)):
        response_msgs.append(json.dumps(
            {
                "recipient": {
                    "id": str(fb_ids[i])
                },
                "messaging_type": "MESSAGE_TAG",  # Messaging type is MESSAGE_TAG, NON_PROMOTIONAL_SUBSCRIPTION
                "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
                "message": message
            })
        )

    CLIENT.send_fb_messages_async(GRAPH_URL, response_msgs)

    if not settings.is_prod():
        logger.log(response_msgs)

    return response_msgs


def send_facebook_message(fb_id, message):
    response_msg = json.dumps(
        {
            "recipient": {
                "id": fb_id
            },
            "messaging_type": "RESPONSE", # Messaging type is RESPONSE
            "message": message
        })

    CLIENT.send_fb_message(GRAPH_URL, response_msg)

    if not settings.is_prod():
        logger.log(response_msg)

    return response_msg


def send_typing(fb_id):
    response_msg = json.dumps(
        {
            "recipient": {
                "id": fb_id
            },
            "messaging_type": "RESPONSE", # Messaging type is RESPONSE
            "sender_action": "typing_on"
        })

    CLIENT.send_fb_message(GRAPH_URL, response_msg)


