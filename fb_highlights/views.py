import json

import dateparser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

import fb_bot.messenger_manager as messenger_manager
from fb_bot import language, analytics
from fb_bot.logger import logger
from fb_bot.messages import EMOJI_TROPHY, EMOJI_CROSS, EMOJI_SMILE, SETTING_CHANGED_MESSAGE, SHOW_BUTTON, HIDE_BUTTON
from fb_bot.model_managers import context_manager, user_manager, football_team_manager, latest_highlight_manager, \
    highlight_stat_manager, highlight_notification_stat_manager, football_competition_manager, \
    registration_competition_manager, new_football_registration_manager, scrapping_status_manager
from fb_bot.model_managers import registration_team_manager
from fb_bot.model_managers.context_manager import ContextType
from fb_highlights import view_message_helper
from fb_highlights.view_message_helper import accepted_messages
from highlights import settings


class DebugPageView(LoginRequiredMixin, TemplateView):
    login_url = '/admin/'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'debug.html')


class Analytics(LoginRequiredMixin, TemplateView):
    login_url = '/admin/'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'analytics.html', analytics.get_highlight_analytics())


class Status(LoginRequiredMixin, TemplateView):
    login_url = '/admin/'

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'status.html', { 'sites': scrapping_status_manager.get_all_scrapping_status() })


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

        # Converts the text payload into a python dictionary
        incoming_message = json.loads(request.body.decode('utf-8'))

        logger.log("Message received: " + str(incoming_message))

        response_msg = []

        for entry in incoming_message['entry']:

            for message in entry['messaging']:

                sender_id = message['sender'].get('id')
                HighlightsBotView.LATEST_SENDER_ID = sender_id

                user_manager.increment_user_message_count(sender_id)

                logger.log_for_user("Message received: " + str(message), sender_id)

                # Events
                if 'message' in message:

                    text = message['message'].get('text') if message['message'].get('text') else ''
                    message = language.remove_accents(text.lower())

                    # Do not respond in those cases
                    if 'no' == message or 'nothing' == message or 'ok' == message or 'shut up' in message or message == '':
                        continue

                    # Send typing event - so user is aware received message
                    messenger_manager.send_typing(sender_id)

                    # Special replies
                    # TODO: remove at some point
                    if message == 'subscribe ' + EMOJI_TROPHY:
                        logger.log_for_user("ADD WORLD CUP", sender_id, forward=True)

                        context_manager.update_context(sender_id, ContextType.SUBSCRIPTIONS_SETTING)

                        registration_competition_manager.add_competition(sender_id, 'world cup')

                        response_msg.append(
                            messenger_manager.send_registration_added_message(sender_id, 'World Cup ' + EMOJI_TROPHY)
                        )

                        response_msg.append(
                            view_message_helper.send_subscriptions_settings(sender_id)
                        )

                    # Special replies
                    # TODO: remove at some point
                    elif message == 'no thanks ' + EMOJI_CROSS:
                        logger.log_for_user("NO THANKS WORLD CUP", sender_id, forward=True)

                        response_msg.append(
                            messenger_manager.send_facebook_message(
                                sender_id, messenger_manager.create_message("Another time! " + EMOJI_SMILE))
                        )

                    # Cancel quick reply
                    elif 'cancel' in message:
                        logger.log("CANCEL")

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            messenger_manager.send_cancel_message(sender_id)
                        )

                    # Done quick reply
                    elif 'done' in message:
                        logger.log("DONE")

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            messenger_manager.send_done_message(sender_id)
                        )

                    # HELP
                    elif 'help' in message:
                        logger.log("HELP")

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            messenger_manager.send_help_message(sender_id)
                        )

                    elif accepted_messages(message, ['thank you', 'thanks', 'cheers', 'merci', 'cimer',
                                                     'good job', 'good bot']):
                        logger.log("THANK YOU MESSAGE")

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            messenger_manager.send_thank_you_message(sender_id)
                        )

                    # TUTORIAL CONTEXT
                    # FIXME: duplication between tutorial and registration team
                    elif context_manager.is_tutorial_context(sender_id):
                        logger.log("TUTORIAL ADD REGISTRATION")

                        registration_to_add = message

                        # Check if team exists, make a recommendation if no teams
                        if registration_to_add == 'other':

                            response_msg.append(
                                messenger_manager.send_getting_started_message_2(sender_id)
                            )

                        elif football_team_manager.has_football_team(registration_to_add):
                            # Does team exist check

                            registration_team_manager.add_team(sender_id, registration_to_add)

                            response_msg.append(
                                messenger_manager.send_tutorial_message(sender_id, text)
                            )

                            response_msg.append(
                                messenger_manager.send_tutorial_highlight(sender_id, registration_to_add)
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_competition_manager.has_football_competition(registration_to_add):
                            # Does competition exist check

                            registration_competition_manager.add_competition(sender_id, registration_to_add)

                            response_msg.append(
                                messenger_manager.send_tutorial_message(sender_id, text)
                            )

                            response_msg.append(
                                messenger_manager.send_tutorial_highlight(sender_id, registration_to_add)
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_team_manager.similar_football_team_names(registration_to_add) \
                            + football_competition_manager.similar_football_competition_names(registration_to_add):
                            # Registration recommendation

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(registration_to_add, 'user')

                            recommendations = football_team_manager.similar_football_team_names(registration_to_add) \
                                              + football_competition_manager.similar_football_competition_names(registration_to_add)

                            # Format recommendation names
                            recommendations = [recommendation.title() for recommendation in recommendations]

                            response_msg.append(
                                messenger_manager.send_recommended_team_tutorial_message(sender_id, recommendations)
                            )

                        else:
                            # No team or recommendation found

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(registration_to_add, 'user')

                            response_msg.append(
                                messenger_manager.send_team_not_found_tutorial_message(sender_id)
                            )

                    # SEE RESULT CHANGE SETTING
                    elif context_manager.is_see_result_setting_context(sender_id):
                        logger.log("SEE RESULT CHANGE SETTING")

                        if text in [SHOW_BUTTON, HIDE_BUTTON]:
                            user_manager.set_see_result_setting(sender_id, text == SHOW_BUTTON)

                            response_msg.append(
                                messenger_manager.send_setting_changed(sender_id)
                            )

                            context_manager.set_default_context(sender_id)

                        else:
                            response_msg.append(
                                messenger_manager.send_setting_invalid(sender_id)
                            )

                            response_msg.append(
                                messenger_manager.send_see_result_setting(sender_id)
                            )

                    # SUBSCRIPTION SETTING
                    elif accepted_messages(message, ['subscription', 'teams', 'subscribe', 'notification']):
                        logger.log("SUBSCRIPTION SETTING")

                        response_msg.append(
                            view_message_helper.send_subscriptions_settings(sender_id)
                        )

                    # ADD REGISTRATION SETTING
                    elif accepted_messages(message, ['add']) and context_manager.is_notifications_setting_context(sender_id):
                        logger.log("ADD REGISTRATION SETTING")

                        context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                        response_msg.append(
                            messenger_manager.send_add_registration_message(sender_id)
                        )

                    # REMOVE REGISTRATION SETTING
                    elif accepted_messages(message, ['remove']) and context_manager.is_notifications_setting_context(sender_id):
                        logger.log("REMOVE REGISTRATION SETTING")

                        context_manager.update_context(sender_id, ContextType.REMOVE_REGISTRATION)

                        registrations = view_message_helper.get_registrations_formatted(sender_id)

                        response_msg.append(
                            messenger_manager.send_delete_registration_message(sender_id, registrations)
                        )

                    # ADDING REGISTRATION
                    # FIXME: duplication between tutorial and registration
                    elif context_manager.is_adding_registration_context(sender_id) \
                            or context_manager.is_notifications_setting_context(sender_id):
                        logger.log("ADDING REGISTRATION")

                        registration_to_add = message

                        # Check if registration exists, make a recommendation if no registration
                        if registration_to_add == 'other' or registration_to_add == 'try again':
                            context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                            response_msg.append(
                                messenger_manager.send_add_registration_message(sender_id)
                            )

                        elif football_team_manager.has_football_team(registration_to_add):
                            # Does team exist check
                            registration_team_manager.add_team(sender_id, registration_to_add)

                            response_msg.append(
                                messenger_manager.send_registration_added_message(sender_id, text)
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_competition_manager.has_football_competition(registration_to_add):
                            # Does competition exist check
                            registration_competition_manager.add_competition(sender_id, registration_to_add)

                            response_msg.append(
                                messenger_manager.send_registration_added_message(sender_id, text)
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_team_manager.similar_football_team_names(registration_to_add) or \
                                football_competition_manager.similar_football_competition_names(registration_to_add):
                            # Registration recommendation
                            context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(registration_to_add, 'user')

                            recommendations = football_team_manager.similar_football_team_names(registration_to_add)\
                                              + football_competition_manager.similar_football_competition_names(registration_to_add)

                            # Format recommendation names
                            recommendations = [recommendation.title() for recommendation in recommendations]

                            response_msg.append(
                                messenger_manager.send_recommended_registration_message(sender_id, recommendations)
                            )

                        else:
                            # No registration recommendation found
                            context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(registration_to_add, 'user')

                            response_msg.append(
                                messenger_manager.send_registration_not_found_message(sender_id)
                            )

                    # REMOVING REGISTRATION
                    elif context_manager.is_deleting_team_context(sender_id):
                        logger.log("REMOVING REGISTRATION")
                        registration_to_delete = message.lower()

                        if football_team_manager.has_football_team(registration_to_delete):
                            # Delete team
                            registration_team_manager.delete_team(sender_id, registration_to_delete)

                            response_msg.append(
                                messenger_manager.send_registration_deleted_message(sender_id, message)
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_competition_manager.has_football_competition(registration_to_delete):
                            # Delete competition
                            registration_competition_manager.delete_competition(sender_id, registration_to_delete)

                            response_msg.append(
                                messenger_manager.send_registration_deleted_message(sender_id, message)
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        else:
                            # Registration to delete not found
                            context_manager.update_context(sender_id, ContextType.REMOVE_REGISTRATION)

                            registrations = view_message_helper.get_registrations_formatted(sender_id)

                            response_msg.append(
                                messenger_manager.send_registration_to_delete_not_found_message(sender_id, registrations)
                            )

                    # SEE RESULT SETTING
                    elif accepted_messages(message, ['see result setting', 'spoiler', 'show result', 'hide result',
                                                     'show score', 'hide score']):
                        logger.log("SEE RESULT SETTING")

                        response_msg.append(
                            view_message_helper.send_send_see_result_settings(sender_id)
                        )

                    # SHARE
                    elif accepted_messages(message, ['share', 'send to a friend']):
                        logger.log("SHARE")

                        response_msg.append(
                            messenger_manager.send_share_introduction_message(sender_id)
                        )
                        response_msg.append(
                            messenger_manager.send_share_message(sender_id)
                        )

                    # SEARCH HIGHLIGHT OPTION
                    elif accepted_messages(message, ['search', 'search again']):
                        logger.log("SEARCH HIGHLIGHTS")

                        response_msg.append(
                            view_message_helper.search_highlights(sender_id)
                        )

                    # SEARCHING HIGHLIGHTS
                    elif context_manager.is_searching_highlights_context(sender_id):
                        logger.log("SEARCHING HIGHLIGHTS")

                        response_msg.append(
                            messenger_manager.send_highlight_message_for_team_or_competition(sender_id, message)
                        )

                if 'postback' in message:
                    postback = message['postback']['payload']

                    if postback == 'get_started':
                        logger.log("GET STARTED POSTBACK")

                        user = user_manager.get_user(sender_id)

                        response_msg.append(
                            messenger_manager.send_getting_started_message(sender_id, user.first_name)
                        )
                        response_msg.append(
                            messenger_manager.send_getting_started_message_2(sender_id)
                        )

                        # Set the user in tutorial context
                        context_manager.update_context(sender_id, ContextType.TUTORIAL_ADD_TEAM)

                    # SEARCH HIGHLIGHT SETTING POSTBACK
                    elif postback == 'search_highlights':
                        logger.log("SEARCH HIGHLIGHTS POSTBACK")

                        response_msg.append(
                            view_message_helper.search_highlights(sender_id)
                        )

                    # SUBSCRIPTION SETTING POSTBACK
                    elif postback == 'my_subscriptions':
                        logger.log("SUBSCRIPTION SETTING POSTBACK")

                        response_msg.append(
                            view_message_helper.send_subscriptions_settings(sender_id)
                        )

                    # SHARE POSTBACK
                    elif postback == 'share':
                        logger.log("SHARE POSTBACK")

                        response_msg.append(
                            messenger_manager.send_share_introduction_message(sender_id)
                        )
                        response_msg.append(
                            messenger_manager.send_share_message(sender_id)
                        )

                    # SEE RESULT SETTING POSTBACK
                    elif postback == 'see_result_setting':
                        logger.log("SEE RESULT SETTING POSTBACK")

                        response_msg.append(
                            view_message_helper.send_send_see_result_settings(sender_id)
                        )

                logger.log_for_user("Message sent: " + str(response_msg), sender_id)
                HighlightsBotView.LATEST_SENDER_ID = 0

        if not settings.DEBUG:
            return HttpResponse()

        else:
            # DEBUG MODE ONLY
            formatted_response = "[" + ", ".join(response_msg) + "]"
            return JsonResponse(formatted_response, safe=False)


class HighlightRedirectView(generic.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        param_keys = ['team1', 'score1', 'team2', 'score2', 'date', 'user_id']

        for param_key in param_keys:
            if param_key not in request.GET:
                return HttpResponseBadRequest('<h1>Invalid link</h1>')

        team1 = request.GET['team1'].lower()
        score1 = int(request.GET['score1'])
        team2 = request.GET['team2'].lower()
        score2 = int(request.GET['score2'])
        date = dateparser.parse(request.GET['date'])
        user_id = int(request.GET['user_id'])

        type = request.GET.get('type')

        # user tracking recording if user clicked on link
        user_manager.increment_user_highlight_click_count(user_id)

        highlight_models = latest_highlight_manager.get_highlights(team1, score1, team2, score2, date)

        if not highlight_models:
            return HttpResponseBadRequest('<h1>Invalid link</h1>')

        extended = type == 'extended'

        if extended:
            # Extended
            highlight_to_send = latest_highlight_manager.get_best_highlight(highlight_models, extended=True)
        else:
            # Short
            highlight_to_send = latest_highlight_manager.get_best_highlight(highlight_models, extended=False)

        # link click tracking
        latest_highlight_manager.increment_click_count(highlight_to_send)

        # Highlight event tracking
        highlight_stat_manager.add_highlight_stat(user_id, highlight_to_send, extended=extended)
        highlight_notification_stat_manager.update_notification_opened(user_id, highlight_to_send)

        return redirect(highlight_to_send.link)
