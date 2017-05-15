import json

from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import fb_bot.messenger_manager as messenger_manager
import highlights.settings
from fb_bot import context_manager
from fb_bot import user_manager
from fb_bot.context_manager import ContextType
from fb_bot.logger import logger


class DebugPageView(TemplateView):
    template_name = "debug.html"


class HighlightsBotView(generic.View):
    LATEST_SENDER_ID = 0

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        if request.GET['hub.verify_token'] == 'ea30725c72d35':
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        logger.log("Message received: " + str(request.body))

        # Converts the text payload into a python dictionary
        incoming_message = json.loads(request.body.decode('utf-8'))

        response_msg = []

        for entry in incoming_message['entry']:

            for message in entry['messaging']:

                sender_id = message['sender']['id']
                HighlightsBotView.LATEST_SENDER_ID = sender_id

                user = user_manager.get_user(sender_id)

                logger.log_for_user("Message received: " + str(message), sender_id)

                # Events
                if 'message' in message:

                    text = message['message']['text']

                    # TODO: use payload to make sure quick reply button used

                    # MENU
                    if 'menu' == text:
                        print("MENU")
                        context_manager.update_context(sender_id, ContextType.MENU)
                        response_msg.append(messenger_manager.send_menu_message(sender_id))

                    # NOTIFICATION SETTING
                    elif 'Notifications' == text and context_manager.is_menu_context(sender_id) :
                        print("NOTIFICATION SETTING")
                        context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)

                        # TODO: fetch teams for user
                        teams = ["Arsenal", "Real madrid"]
                        response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                    # ADD TEAM SETTING
                    elif 'Add' == text and context_manager.is_notifications_setting_context(sender_id):
                        print("ADD TEAM SETTING")
                        context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                        response_msg.append(messenger_manager.send_add_team_message(sender_id))

                    # DELETE TEAM SETTING
                    elif 'Delete' == text and context_manager.is_notifications_setting_context(sender_id):
                        print("DELETE TEAM SETTING")
                        # TODO: fetch teams for user
                        teams = ["Arsenal", "Real madrid"]
                        context_manager.update_context(sender_id, ContextType.DELETING_TEAM)

                        response_msg.append(messenger_manager.send_delete_team_message(sender_id, teams))

                    # ADDING TEAM
                    elif context_manager.is_adding_team_context(sender_id):
                        print("ADDING TEAM")
                        # TODO: check if team exists
                        response_msg.append(messenger_manager.send_team_added_message(sender_id, True, text))

                        # TODO: fetch teams for user
                        teams = ["Arsenal", "Real madrid"]
                        context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)
                        response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                    # DELETING TEAM
                    elif context_manager.is_deleting_team_context(sender_id):
                        print("DELETING TEAM")
                        response_msg.append(messenger_manager.send_team_deleted_message(sender_id, text))

                        # TODO: fetch teams for user
                        teams = ["Arsenal", "Real madrid"]
                        context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)
                        response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                    # SEARCH FOR TEAM
                    else:
                        print("SEARCH FOR TEAM")
                        context_manager.update_context(sender_id, ContextType.NONE)
                        response_msg.append(messenger_manager.send_highlight_message_for_team(sender_id, text))

                elif 'postback' in message:
                    postback = message['postback']['payload']

                    if postback == 'get_started':
                        response_msg.append(messenger_manager.send_getting_started_message(sender_id))

                    elif postback == 'recent':
                        response_msg.append(messenger_manager.send_highlight_message_recent(sender_id))

                    elif postback == 'popular':
                        response_msg.append(messenger_manager.send_highlight_message_popular(sender_id))

                logger.log_for_user("Message sent: " + str(response_msg), sender_id)
                HighlightsBotView.LATEST_SENDER_ID = 0

        if not highlights.settings.DEBUG:
            return HttpResponse()

        # For DEBUG MODE only
        formatted_response = "["

        for i in range(len(response_msg)):
            formatted_response += response_msg[i]

            if i != len(response_msg) - 1:
                formatted_response += ", "

        formatted_response += "]"

        return JsonResponse(formatted_response, safe=False)