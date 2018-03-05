from concurrent.futures import ThreadPoolExecutor

import requests
from requests import Timeout


def send_fb_messages_async(url, messages):

    def send(message):
        return send_fb_message(url, message)

    with ThreadPoolExecutor(max_workers=20) as executor:
        responses = executor.map(send, messages)

    return responses


def send_fb_message(url, message):
    try:
        return requests.post(url, headers={"Content-Type": "application/json"}, data=message)
    except Timeout:
        pass