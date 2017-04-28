import highlights_fetcher
import json

import requests
from django.utils.decorators import method_decorator
from django.views import generic
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

ACCESS_TOKEN = 'EAAJvTnLYbnkBANP32ZCoDdyBw2nMvZAQ9vkHORylXFouyhvvv4VJ65DUPncr0RpeDZCzDtCb1FUoNFA9Ayq8STkMLXMKtAVIY0Udg3EZCzNtc6BcFdcvMzZCZC7ZBHBvZCZCZC1a1QRwgKfAMorFdHcoeqa5YphsvKXFdOZBggUCHFAIgZDZD'


class HighlightsBotView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        if self.request.GET['hub.verify_token'] == 'ea30725c72d35':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        print(self.request.body)

        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:

            for message in entry['messaging']:

                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    print(message)

                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    post_facebook_message(message['sender']['id'], message['message']['text'])

        return HttpResponse()


def post_facebook_message(fb_id, received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({"recipient":
                                   {"id": fb_id},
                                   "message": "j"
                               })

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)

    print(status.json())


def get_highlights():
    return { "attachment":{
         "type":"template",
         "payload": {
            "template_type": "list",
            "top_element_style": "compact",
            "elements": get_elements()
         }
      }
    }


def get_elements():
    elems = []
    highlights = highlights_fetcher.fetch_highlights()

    # TODO: Get the 4 most popular highlight videos
    # highlights.sort(key=lambda highlight: highlight.view_count)

    for i in range(4):
        link, match_name, img_link, view_count, category, time_since_added = highlights[i]

        elems.append({
                  "title": match_name,
                  "image_url": img_link,
                  "subtitle": time_since_added,
                  "default_action":{
                     "type": "web_url",
                     "url": link,
                     "messenger_extensions": "false",
                     "webview_height_ratio": "full"
                  }
               })

    return json.dumps(elems)