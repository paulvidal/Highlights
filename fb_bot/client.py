from concurrent.futures import ThreadPoolExecutor

import requests
from requests import Timeout

from fb_bot.logger import logger
from highlights import settings


class Client:

    def __init__(self):
        self.client_send = not settings.DEBUG
        self.messages = []

    def disable(self):
        # Used for testing
        self.client_send = False

    def send_fb_messages_async(self, url, messages):

        def send(message):
            return self.send_fb_message(url, message)

        with ThreadPoolExecutor(max_workers=50) as executor:
            responses = executor.map(send, messages)

        return responses

    def send_fb_message(self, url, message):
        if self.client_send:
            try:
                return requests.post(url, headers={"Content-Type": "application/json"}, data=message)
            except Timeout:
                logger.log("Message timeout to send: " + str(message), forward=True)

        else:
            self.messages.append(message)