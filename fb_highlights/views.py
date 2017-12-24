import json

from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import fb_bot.messenger_manager as messenger_manager
import highlights.settings
from fb_bot.logger import logger
from fb_bot.model_managers import context_manager, user_manager, football_team_manager
from fb_bot.model_managers import team_manager
from fb_bot.model_managers.context_manager import ContextType


class DebugPageView(TemplateView):
    template_name = "debug.html"


class PrivacyPageView(TemplateView):
    template_name = "privacy.html"


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

                # Send typing event - so user is aware received message
                messenger_manager.send_typing(sender_id)

                user_manager.increment_user_message_count(sender_id)

                logger.log_for_user("Message received: " + str(message), sender_id)

                # Events
                if 'message' in message:

                    text = message['message']['text']

                    # Cancel quick reply
                    if 'cancel' == text.lower():
                        print("CANCEL")
                        context_manager.update_context(sender_id, ContextType.NONE)

                    # MENU
                    elif 'menu' == text.lower():
                        print("MENU")
                        context_manager.update_context(sender_id, ContextType.MENU)

                        response_msg.append(messenger_manager.send_menu_message(sender_id))

                    # NOTIFICATION SETTING
                    elif 'Notifications' == text and context_manager.is_menu_context(sender_id) :
                        print("NOTIFICATION SETTING")
                        context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)

                        teams = team_manager.get_teams_for_user(sender_id)
                        # Format team names
                        teams = [team.title() for team in teams]

                        response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                    # ADD TEAM SETTING
                    elif 'Add' == text and context_manager.is_notifications_setting_context(sender_id):
                        print("ADD TEAM SETTING")
                        context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                        response_msg.append(messenger_manager.send_add_team_message(sender_id))

                    # DELETE TEAM SETTING
                    elif 'Delete' == text and context_manager.is_notifications_setting_context(sender_id):
                        print("DELETE TEAM SETTING")
                        context_manager.update_context(sender_id, ContextType.DELETING_TEAM)

                        teams = team_manager.get_teams_for_user(sender_id)
                        # Format team names
                        teams = [team.title() for team in teams]

                        response_msg.append(messenger_manager.send_delete_team_message(sender_id, teams))

                    # ADDING TEAM
                    elif context_manager.is_adding_team_context(sender_id):
                        print("ADDING TEAM")

                        team_to_add = text.lower()

                        # Check if team exists, make a recommendation if no teams
                        if team_to_add == 'other':
                            context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                            response_msg.append(messenger_manager.send_add_team_message(sender_id))

                        elif football_team_manager.has_football_team(team_to_add):
                            # Does team exist check
                            context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)

                            team_manager.add_team(sender_id, team_to_add)
                            response_msg.append(messenger_manager.send_team_added_message(sender_id, True, text))

                            teams = team_manager.get_teams_for_user(sender_id)
                            # Format team names
                            teams = [team.title() for team in teams]

                            response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                        elif football_team_manager.similar_football_teams(team_to_add):
                            # Team recommendation
                            context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                            recommendations = football_team_manager.similar_football_teams(team_to_add)[:messenger_manager.MAX_QUICK_REPLIES]
                            # Format recommendation names
                            recommendations = [recommendation.title() for recommendation in recommendations]

                            response_msg.append(messenger_manager.send_recommended_team_messages(sender_id, recommendations))

                        else:
                            # No team or recommendation found
                            context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                            response_msg.append(messenger_manager.send_team_not_found_message(sender_id))

                    # DELETING TEAM
                    elif context_manager.is_deleting_team_context(sender_id):
                        print("DELETING TEAM")
                        team_to_delete = text.lower()

                        if football_team_manager.has_football_team(team_to_delete):
                            # Delete team
                            team_manager.delete_team(sender_id, team_to_delete)
                            response_msg.append(messenger_manager.send_team_deleted_message(sender_id, text))

                            teams = team_manager.get_teams_for_user(sender_id)
                            # Format team names
                            teams = [team.title() for team in teams]

                            context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)
                            response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                        else:
                            # Team to delete not found
                            context_manager.update_context(sender_id, ContextType.DELETING_TEAM)

                            teams = team_manager.get_teams_for_user(sender_id)
                            # Format team names
                            teams = [team.title() for team in teams]

                            response_msg.append(messenger_manager.send_team_to_delete_not_found_message(sender_id, teams))

                    # LATEST HIGHLIGHTS
                    elif 'Latest Highlights' == text:
                        response_msg.append(messenger_manager.send_highlight_message_recent(sender_id))

                    # POPULAR HIGHLIGHTS
                    elif 'Popular Highlights' == text:
                        response_msg.append(messenger_manager.send_highlight_message_popular(sender_id))

                    # HELP
                    elif 'help' in text.lower():
                        print("HELP")
                        response_msg.append(messenger_manager.send_help_message(sender_id))

                    # SEARCH FOR TEAM
                    else:
                        print("SEARCH FOR TEAM")
                        context_manager.update_context(sender_id, ContextType.NONE)

                        response_msg.append(messenger_manager.send_highlight_message_for_team(sender_id, text))

                elif 'postback' in message:
                    postback = message['postback']['payload']

                    if postback == 'get_started':
                        user = user_manager.get_user(sender_id)
                        response_msg.append(messenger_manager.send_getting_started_message(sender_id, user.first_name))

                        # Set the user in add a team context
                        context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

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