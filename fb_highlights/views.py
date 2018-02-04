import json

import dateparser
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import fb_bot.messenger_manager as messenger_manager
from highlights import settings
from fb_bot.logger import logger
from fb_bot.model_managers import context_manager, user_manager, football_team_manager, latest_highlight_manager, \
    highlight_stat_manager, highlight_notification_stat_manager
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

                sender_id = message['sender'].get('id')
                HighlightsBotView.LATEST_SENDER_ID = sender_id

                # Send typing event - so user is aware received message
                messenger_manager.send_typing(sender_id)

                user_manager.increment_user_message_count(sender_id)

                logger.log_for_user("Message received: " + str(message), sender_id)

                # Events
                if 'message' in message:

                    text = message['message'].get('text') if message['message'].get('text') else ''
                    message = text.lower()

                    # Cancel quick reply
                    if 'cancel' in message:
                        print("CANCEL")
                        context_manager.update_context(sender_id, ContextType.NONE)

                        response_msg.append(messenger_manager.send_cancel_message(sender_id))

                        # Answer with new message what want to do
                        response_msg.append(messenger_manager.send_anything_else_i_can_do_message(sender_id))

                    # Done quick reply
                    elif 'done' in message:
                        print("DONE")
                        context_manager.update_context(sender_id, ContextType.NONE)

                        response_msg.append(messenger_manager.send_done_message(sender_id))

                        # Answer with new message what want to do
                        response_msg.append(messenger_manager.send_anything_else_i_can_do_message(sender_id))

                    # HELP
                    elif 'help' in message:
                        print("HELP")
                        context_manager.update_context(sender_id, ContextType.NONE)

                        response_msg.append(messenger_manager.send_help_message(sender_id))

                    elif 'thank you' in message or 'thanks' in message or 'cheers' in message:
                        print("THANK YOU MESSAGE")
                        context_manager.update_context(sender_id, ContextType.NONE)

                        response_msg.append(messenger_manager.send_than_you_message(sender_id))

                    # TUTORIAL CONTEXT
                    # FIXME: duplication between tutorial and adding team
                    elif context_manager.is_tutorial_context(sender_id):
                        print("TUTORIAL")

                        if context_manager.is_tutorial_add_team_context(sender_id):
                            print("TUTORIAL ADD TEAM")

                            team_to_add = message

                            # Check if team exists, make a recommendation if no teams
                            if team_to_add == 'other':
                                response_msg.append(messenger_manager.send_add_team_message(sender_id))

                            elif football_team_manager.has_football_team(team_to_add):
                                # Does team exist check

                                team_manager.add_team(sender_id, team_to_add)

                                response_msg.append(messenger_manager.send_tutorial_message_1(sender_id, text))
                                response_msg.append(messenger_manager.send_tutorial_highlight(sender_id, team_to_add))

                                context_manager.update_context(sender_id, ContextType.TUTORIAL_UNDERSTOOD)

                                response_msg.append(messenger_manager.send_tutorial_message_2(sender_id))

                            elif football_team_manager.similar_football_team_names(team_to_add):
                                # Team recommendation

                                recommendations = football_team_manager.similar_football_team_names(team_to_add)[:messenger_manager.MAX_QUICK_REPLIES]
                                # Format recommendation names
                                recommendations = [recommendation.title() for recommendation in recommendations]

                                response_msg.append(messenger_manager.send_recommended_team_tutorial_message(sender_id, recommendations))

                            else:
                                # No team or recommendation found

                                response_msg.append(messenger_manager.send_team_not_found_tutorial_message(sender_id))

                        elif context_manager.is_tutorial_understood_context(sender_id):
                            print("TUTORIAL UNDERSTOOD")

                            response_msg.append(messenger_manager.send_tutorial_message_3(sender_id))

                            # Send notification menu
                            context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)

                            teams = team_manager.get_teams_for_user(sender_id)
                            # Format team names
                            teams = [team.title() for team in teams]

                            response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                    # SEARCH HIGHLIGHT OPTION
                    elif 'search highlights' in message or 'search again' in message:
                        print("SEARCH HIGHLIGHTS")
                        context_manager.update_context(sender_id, ContextType.SEARCH_HIGHLIGHTS)

                        response_msg.append(messenger_manager.send_search_highlights_message(sender_id))

                    # SEARCHING HIGHLIGHTS
                    elif context_manager.is_searching_highlights_context(sender_id):
                        print("SEARCHING HIGHLIGHTS")
                        team_found = messenger_manager.has_highlight_for_team(message)

                        response_msg.append(messenger_manager.send_highlight_message_for_team(sender_id, message))

                        if team_found:
                            context_manager.update_context(sender_id, ContextType.NONE)

                            # Answer with new message what want to do
                            response_msg.append(messenger_manager.send_anything_else_i_can_do_message(sender_id))

                        else:
                            context_manager.update_context(sender_id, ContextType.SEARCH_HIGHLIGHTS)

                    # NOTIFICATION SETTING
                    elif 'my teams' in message:
                        print("NOTIFICATION SETTING")
                        context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)

                        teams = team_manager.get_teams_for_user(sender_id)
                        # Format team names
                        teams = [team.title() for team in teams]

                        response_msg.append(messenger_manager.send_notification_message(sender_id, teams))

                    # ADD TEAM SETTING
                    elif 'add' in message and context_manager.is_notifications_setting_context(sender_id):
                        print("ADD TEAM SETTING")
                        context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                        response_msg.append(messenger_manager.send_add_team_message(sender_id))

                    # REMOVE TEAM SETTING
                    elif 'remove' in message and context_manager.is_notifications_setting_context(sender_id):
                        print("REMOVE TEAM SETTING")
                        context_manager.update_context(sender_id, ContextType.DELETING_TEAM)

                        teams = team_manager.get_teams_for_user(sender_id)
                        # Format team names
                        teams = [team.title() for team in teams]

                        response_msg.append(messenger_manager.send_delete_team_message(sender_id, teams))

                    # ADDING TEAM
                    # FIXME: duplication between tutorial and adding team
                    elif context_manager.is_adding_team_context(sender_id):
                        print("ADDING TEAM")

                        team_to_add = message

                        # Check if team exists, make a recommendation if no teams
                        if team_to_add == 'other' or team_to_add == 'try again':
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

                        elif football_team_manager.similar_football_team_names(team_to_add):
                            # Team recommendation
                            context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                            recommendations = football_team_manager.similar_football_team_names(team_to_add)[:messenger_manager.MAX_QUICK_REPLIES]
                            # Format recommendation names
                            recommendations = [recommendation.title() for recommendation in recommendations]

                            response_msg.append(messenger_manager.send_recommended_team_message(sender_id, recommendations))

                        else:
                            # No team or recommendation found
                            context_manager.update_context(sender_id, ContextType.ADDING_TEAM)

                            response_msg.append(messenger_manager.send_team_not_found_message(sender_id))

                    # DELETING TEAM
                    elif context_manager.is_deleting_team_context(sender_id):
                        print("DELETING TEAM")
                        team_to_delete = message.lower()

                        if football_team_manager.has_football_team(team_to_delete):
                            # Delete team
                            team_manager.delete_team(sender_id, team_to_delete)
                            response_msg.append(messenger_manager.send_team_deleted_message(sender_id, message))

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

                    # IF NO MATCH, UNLESS NAME OF A TEAM IS TYPED, ASK WHAT WANT TO DO
                    else:
                        context_manager.update_context(sender_id, ContextType.NONE)

                        team_found = messenger_manager.has_highlight_for_team(message)

                        if team_found:
                            # FIXME: duplication with searching highlights
                            print("NO MATCH - SEARCHING HIGHLIGHTS")
                            response_msg.append(messenger_manager.send_highlight_message_for_team(sender_id, message))

                            # Answer with new message what want to do
                            response_msg.append(messenger_manager.send_anything_else_i_can_do_message(sender_id))

                        else:
                            print("WHAT WANT TO DO")
                            response_msg.append(messenger_manager.send_what_do_you_want_to_do_message(sender_id))

                elif 'postback' in message:
                    postback = message['postback']['payload']

                    if postback == 'get_started':
                        user = user_manager.get_user(sender_id)

                        response_msg.append(messenger_manager.send_getting_started_message(sender_id, user.first_name))
                        response_msg.append(messenger_manager.send_getting_started_message_2(sender_id))

                        # Set the user in tutorial context
                        context_manager.update_context(sender_id, ContextType.TUTORIAL_ADD_TEAM)

                logger.log_for_user("Message sent: " + str(response_msg), sender_id)
                HighlightsBotView.LATEST_SENDER_ID = 0

        if not settings.DEBUG:
            return HttpResponse()

        # For DEBUG MODE only
        formatted_response = "["

        for i in range(len(response_msg)):
            formatted_response += response_msg[i]

            if i != len(response_msg) - 1:
                formatted_response += ", "

        formatted_response += "]"

        return JsonResponse(formatted_response, safe=False)


class HighlightRedirectView(generic.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        param_keys = ['team1', 'score1', 'team2', 'score2', 'date', 'user_id']

        for param_key in param_keys:
            if param_key not in request.GET:
                return HttpResponse('Invalid link')

        team1 = request.GET['team1'].lower()
        score1 = int(request.GET['score1'])
        team2 = request.GET['team2'].lower()
        score2 = int(request.GET['score2'])
        date = dateparser.parse(request.GET['date'])
        user_id = int(request.GET['user_id'])

        # user tracking recording if user clicked on link
        user_manager.increment_user_highlight_click_count(user_id)

        highlight_models = latest_highlight_manager.get_highlights(team1, score1, team2, score2, date)
        highlight_to_send = latest_highlight_manager.get_best_highlight(highlight_models)

        # link click tracking
        latest_highlight_manager.increment_click_count(highlight_to_send)

        # Highlight event tracking
        highlight_stat_manager.add_highlight_stat(user_id, highlight_to_send)
        highlight_notification_stat_manager.update_notification_opened(user_id, highlight_to_send)

        return redirect(highlight_to_send.link)
