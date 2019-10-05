from concurrent.futures import ThreadPoolExecutor

import requests
from requests import Timeout

from fb_bot.logger import logger
from highlights import env


class Client:

    def __init__(self):
        self.client_send = not env.DEBUG
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
                response = requests.post(url, headers={"Content-Type": "application/json"}, data=message)

                if response.status_code != 200:
                    logger.warning("Facebook message sending error", extra={
                        'url': url,
                        'content': str(response.content),
                        'response_code': response.status_code
                    })
                else:
                    logger.info("Facebook message sending success", extra={
                        'url': url,
                        'content': str(response.content),
                        'response_code': response.status_code
                    })

            except Timeout:
                logger.error("Facebook message sending timed out", extra={
                    'url': url,
                    'data': message
                })
            except:
                logger.error("Facebook message sending failed", extra={
                    'url': url,
                    'data': message
                })

        else:
            self.messages.append(message)