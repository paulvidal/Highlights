import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from fb_bot import language, analytics
from fb_bot.highlight_fetchers.info import providers
from fb_bot.logger import logger
from fb_bot.messages import EMOJI_CROSS, EMOJI_SMILE, SHOW_BUTTON, HIDE_BUTTON, \
    OTHER_BUTTON, TRY_AGAIN_BUTTON, I_M_GOOD_BUTTON, EMOJI_TROPHY
from fb_bot.messenger_manager import manager_response, manager_highlights, sender, manager_share
from fb_bot.messenger_manager.formatter_highlights import create_link
from fb_bot.model_managers import context_manager, user_manager, football_team_manager, latest_highlight_manager, \
    highlight_stat_manager, highlight_notification_stat_manager, football_competition_manager, \
    registration_competition_manager, new_football_registration_manager, scrapping_status_manager, \
    recommendation_manager
from fb_bot.model_managers import registration_team_manager
from fb_bot.model_managers.context_manager import ContextType
from fb_bot.recomendations import recommendation_engine
from fb_highlights import view_message_helper
from fb_highlights.view_message_helper import accepted_messages
from highlights import env
from monitoring import metrics


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


class Index(TemplateView):
    template_name = "index.html"


class PrivacyPageView(TemplateView):
    template_name = "privacy.html"


class HighlightsView(generic.View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        search = request.GET.get('search').lower() if request.GET.get('search') else None
        count = int(request.GET.get('count')) if request.GET.get('count') else 12

        response = latest_highlight_manager.get_recent_unique_highlights(count, search)
        suggestions = []

        if not response:
            suggestions = football_team_manager.similar_football_team_names(search) \
                          + football_competition_manager.similar_football_competition_names(search)

        for h in response:
            h['link'] = create_link(h['id'], extended=False)
            h['link_extended'] = create_link(h['id'], extended=True)

        return JsonResponse({
            'highlights': response,
            'suggestions': suggestions
        })


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

        logger.info("Message received", extra={
            'incoming_message': incoming_message
        })

        response_msg = []

        for entry in incoming_message['entry']:

            for message in entry['messaging']:

                sender_id = message['sender'].get('id')
                HighlightsBotView.LATEST_SENDER_ID = sender_id

                user = user_manager.get_user(sender_id)
                user_manager.increment_user_message_count(sender_id)

                logger.log_for_user("Message received", sender_id, extra={
                    'full_msg': message
                })

                metric_tags = []

                # Events
                if 'message' in message:

                    text = message['message'].get('text') if message['message'].get('text') else ''
                    message = language.remove_accents(text.lower())

                    logger.log_for_user("Text message received", sender_id, extra={
                        'full_msg': message,
                        'msg_type': 'message'
                    })
                    metric_tags.append('type:message')

                    # Do not respond in those cases
                    if 'no' == message or 'nothing' == message or 'ok' == message or 'shut up' in message or message == '':
                        logger.log_for_user('No response', sender_id)
                        metric_tags.append('action:nothing')
                        continue

                    # Send typing event - so user is aware received message
                    sender.send_typing(sender_id)

                    # Special replies
                    # TODO: remove at some point
                    if message == EMOJI_TROPHY + ' add nations league':
                        logger.log_for_user("ADD NATIONS LEAGUE", sender_id)

                        context_manager.update_context(sender_id, ContextType.SUBSCRIPTIONS_SETTING)

                        registration_competition_manager.add_competition(sender_id, 'nations league')

                        response_msg.append(
                            manager_response.send_registration_added_message(sender_id, 'Nations League')
                        )

                        response_msg.append(
                            view_message_helper.send_subscriptions_settings(sender_id)
                        )

                    # Special replies
                    # TODO: remove at some point
                    elif message == EMOJI_CROSS + ' no thanks':
                        logger.log_for_user("NO THANKS NATIONS LEAGUE", sender_id)

                        response_msg.append(
                            manager_response.send_facebook_message(
                                sender_id, manager_response.create_message("Another time! " + EMOJI_SMILE))
                        )

                    # Cancel quick reply
                    elif 'cancel' in message:
                        logger.log_for_user("CANCEL", sender_id)
                        metric_tags.append('action:cancel')

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            manager_response.send_cancel_message(sender_id)
                        )

                    # Done quick reply
                    elif 'done' in message:
                        logger.log_for_user("DONE", sender_id)
                        metric_tags.append('action:done')

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            manager_response.send_done_message(sender_id)
                        )

                    # HELP
                    elif 'help' in message:
                        logger.log_for_user("HELP", sender_id)
                        metric_tags.append('action:help')

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            manager_response.send_help_message(sender_id)
                        )

                    elif accepted_messages(message, ['thank you', 'thanks', 'cheers', 'merci', 'cimer',
                                                     'good job', 'good bot']):
                        logger.log_for_user("THANK YOU MESSAGE", sender_id)
                        metric_tags.append('action:thank_you')

                        context_manager.set_default_context(sender_id)
                        response_msg.append(
                            manager_response.send_thank_you_message(sender_id)
                        )

                    # TUTORIAL CONTEXT
                    elif context_manager.is_tutorial_context(sender_id):
                        logger.log_for_user("TUTORIAL ADD REGISTRATION", sender_id, extra={
                            'action': 'tutorial'
                        })
                        metric_tags.append('action:tutorial')

                        message = message

                        # Check if team exists, make a recommendation if no teams
                        if football_team_manager.has_football_team(message):
                            # Does team exist check

                            registration_team_manager.add_team(sender_id, message)

                            response_msg.append(
                                manager_highlights.send_tutorial_message(sender_id, text)
                            )

                            response_msg.append(
                                manager_highlights.send_highlights_for_team_or_competition(sender_id,
                                                                                           message,
                                                                                           highlight_count=1,
                                                                                           default_teams=['psg', 'barcelona', 'real madrid', 'spain', 'france'])
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_competition_manager.has_football_competition(message):
                            # Does competition exist check

                            registration_competition_manager.add_competition(sender_id, message)

                            response_msg.append(
                                manager_highlights.send_tutorial_message(sender_id, text)
                            )

                            response_msg.append(
                                manager_highlights.send_highlights_for_team_or_competition(sender_id,
                                                                                           message,
                                                                                           highlight_count=1,
                                                                                           default_teams=['psg', 'barcelona', 'real madrid', 'spain', 'france'])
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_team_manager.similar_football_team_names(message) \
                            + football_competition_manager.similar_football_competition_names(message):
                            # Registration recommendation

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(message, 'user', user)

                            recommendations = football_team_manager.similar_football_team_names(message) \
                                              + football_competition_manager.similar_football_competition_names(message)

                            # Format recommendation names
                            recommendations = [recommendation.title() for recommendation in recommendations]

                            response_msg.append(
                                manager_highlights.send_recommended_team_or_competition_tutorial_message(sender_id, recommendations)
                            )

                        else:
                            # No team or recommendation found

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(message, 'user', user)

                            response_msg.append(
                                manager_highlights.send_team_not_found_tutorial_message(sender_id)
                            )

                    # SEE RESULT CHANGE SETTING
                    elif context_manager.is_see_result_setting_context(sender_id):
                        logger.log_for_user("SEE RESULT CHANGE SETTING", sender_id)
                        metric_tags.append('action:change_setting_see_result')

                        if text in [SHOW_BUTTON, HIDE_BUTTON]:
                            user_manager.set_see_result_setting(sender_id, text == SHOW_BUTTON)

                            response_msg.append(
                                manager_response.send_setting_changed(sender_id)
                            )

                            context_manager.set_default_context(sender_id)

                        else:
                            response_msg.append(
                                manager_response.send_setting_invalid(sender_id)
                            )

                            response_msg.append(
                                manager_response.send_see_result_setting(sender_id)
                            )

                    # ADD REGISTRATION SETTING
                    elif accepted_messages(message, ['add']) and context_manager.is_notifications_setting_context(sender_id):
                        logger.log_for_user("ADD REGISTRATION SETTING", sender_id)
                        metric_tags.append('action:add_registration')

                        context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                        response_msg.append(
                            manager_response.send_add_registration_message(sender_id)
                        )

                    # REMOVE REGISTRATION SETTING
                    elif accepted_messages(message, ['remove']) and context_manager.is_notifications_setting_context(sender_id):
                        logger.log_for_user("REMOVE REGISTRATION SETTING", sender_id)
                        metric_tags.append('action:remove_registration')

                        context_manager.update_context(sender_id, ContextType.REMOVE_REGISTRATION)

                        registrations = view_message_helper.get_registrations_formatted(sender_id)

                        response_msg.append(
                            manager_response.send_delete_registration_message(sender_id, registrations)
                        )

                    # ADDING REGISTRATION
                    elif context_manager.is_adding_registration_context(sender_id) \
                            or context_manager.is_notifications_setting_context(sender_id):
                        logger.log_for_user("ADDING REGISTRATION", sender_id)
                        metric_tags.append('action:adding_registration')

                        message = message

                        # Check if registration exists, make a recommendation if no registration
                        if message == OTHER_BUTTON.lower() or message == TRY_AGAIN_BUTTON.lower():
                            context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                            response_msg.append(
                                manager_response.send_add_registration_message(sender_id)
                            )

                        elif accepted_messages(message, [I_M_GOOD_BUTTON.lower(), 'stop', 'done', 'good']):
                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_team_manager.has_football_team(message):
                            # Does team exist check
                            registration_team_manager.add_team(sender_id, message)

                            response_msg.append(
                                manager_response.send_registration_added_message(sender_id, text)
                            )

                            response_msg.append(
                                manager_response.send_add_registration_message(sender_id)
                            )

                        elif football_competition_manager.has_football_competition(message):
                            # Does competition exist check
                            registration_competition_manager.add_competition(sender_id, message)

                            response_msg.append(
                                manager_response.send_registration_added_message(sender_id, text)
                            )

                            response_msg.append(
                                manager_response.send_add_registration_message(sender_id)
                            )

                        elif football_team_manager.similar_football_team_names(message) or \
                                football_competition_manager.similar_football_competition_names(message):
                            # Registration recommendation
                            context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(message, 'user', user)

                            recommendations = football_team_manager.similar_football_team_names(message)\
                                              + football_competition_manager.similar_football_competition_names(message)

                            # Format recommendation names
                            recommendations = [recommendation.title() for recommendation in recommendations]

                            response_msg.append(
                                manager_response.send_recommended_registration_message(sender_id, recommendations)
                            )

                        else:
                            # No registration recommendation found
                            context_manager.update_context(sender_id, ContextType.ADDING_REGISTRATION)

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(message, 'user', user)

                            response_msg.append(
                                manager_response.send_registration_not_found_message(sender_id)
                            )

                    # REMOVING REGISTRATION
                    elif context_manager.is_deleting_team_context(sender_id):
                        logger.log_for_user("REMOVING REGISTRATION", sender_id)
                        metric_tags.append('action:removing_registration')
                        registration_to_delete = message.lower()

                        if football_team_manager.has_football_team(registration_to_delete):
                            # Delete team
                            registration_team_manager.delete_team(sender_id, registration_to_delete)

                            response_msg.append(
                                manager_response.send_registration_deleted_message(sender_id, registration_to_delete.title())
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        elif football_competition_manager.has_football_competition(registration_to_delete):
                            # Delete competition
                            registration_competition_manager.delete_competition(sender_id, registration_to_delete)

                            response_msg.append(
                                manager_response.send_registration_deleted_message(sender_id, registration_to_delete.title())
                            )

                            response_msg.append(
                                view_message_helper.send_subscriptions_settings(sender_id)
                            )

                        else:
                            # Registration to delete not found
                            context_manager.update_context(sender_id, ContextType.REMOVE_REGISTRATION)

                            registrations = view_message_helper.get_registrations_formatted(sender_id)

                            response_msg.append(
                                manager_response.send_registration_to_delete_not_found_message(sender_id, registrations)
                            )

                    # SUBSCRIPTION SETTING
                    elif accepted_messages(message, ['subscription', 'teams', 'subscribe', 'notification', 'add', 'remove']):
                        logger.log_for_user("SUBSCRIPTION SETTING", sender_id, extra={
                            'action': 'subscriptions'
                        })
                        metric_tags.append('action:see_subscriptions')

                        response_msg.append(
                            view_message_helper.send_subscriptions_settings(sender_id)
                        )

                    # SEE RESULT SETTING
                    elif accepted_messages(message, ['settings', 'see result setting', 'spoiler', 'show result', 'hide result',
                                                     'show score', 'hide score', 'no score']):
                        logger.log_for_user("SEE RESULT SETTING", sender_id, extra={
                            'action': 'settings'
                        })
                        metric_tags.append('action:see_result_setting')

                        response_msg.append(
                            view_message_helper.send_send_see_result_settings(sender_id)
                        )

                    # SHARE
                    elif accepted_messages(message, ['share', 'send to a friend']):
                        logger.log_for_user("SHARE", sender_id, extra={
                            'action': 'share'
                        })
                        metric_tags.append('action:share')
                        metric_tags.append('user_id:{}'.format(sender_id))

                        response_msg.append(
                            manager_share.send_share_introduction_message(sender_id)
                        )
                        response_msg.append(
                            manager_share.send_share_message(sender_id)
                        )

                    # SEARCH HIGHLIGHT OPTION
                    elif accepted_messages(message, ['search', 'search again']):
                        logger.log_for_user("SEARCH HIGHLIGHTS", sender_id, extra={
                            'action': 'search'
                        })
                        metric_tags.append('action:search')

                        response_msg.append(
                            view_message_helper.search_highlights(sender_id)
                        )

                    # SEARCHING HIGHLIGHTS
                    elif context_manager.is_searching_highlights_context(sender_id):
                        logger.log_for_user("SEARCHING HIGHLIGHTS", sender_id, extra={
                            'action': 'searching'
                        })
                        metric_tags.append('action:searching')

                        team_or_competition = message

                        if football_team_manager.has_football_team(team_or_competition) \
                                or football_competition_manager.has_football_competition(team_or_competition):
                            # Team or competition found

                            response_msg.append(
                                manager_highlights.send_highlights_for_team_or_competition(sender_id, team_or_competition)
                            )

                        elif football_team_manager.similar_football_team_names(team_or_competition) \
                                + football_competition_manager.similar_football_competition_names(team_or_competition):
                            # Recommendation found

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(team_or_competition, 'user', user)

                            recommendations = football_team_manager.similar_football_team_names(team_or_competition) \
                                              + football_competition_manager.similar_football_competition_names(team_or_competition)

                            if len(recommendations) == 1:
                                response_msg.append(
                                    manager_highlights.send_highlights_for_team_or_competition(sender_id, recommendations[0])
                                )

                            else:
                                # Format recommendation names
                                recommendations = [recommendation.title() for recommendation in recommendations]

                                response_msg.append(
                                    manager_highlights.send_recommended_team_or_competition_message(sender_id, recommendations)
                                )

                        else:
                            # No team or recommendation found

                            # Register wrong search
                            new_football_registration_manager.add_football_registration(team_or_competition, 'user', user)

                            response_msg.append(
                                manager_highlights.send_team_not_found_tutorial_message(sender_id)
                            )

                if 'postback' in message:
                    postback = message['postback']['payload']

                    logger.log_for_user("Postback message received", sender_id, extra={
                        'full_msg': message,
                        'msg_type': 'postback'
                    })
                    metric_tags.append('type:postback')

                    if postback == 'get_started':
                        logger.log_for_user("GET STARTED POSTBACK", sender_id, extra={
                            'action': 'start'
                        })
                        metric_tags.append('action:get_started')

                        response_msg.append(
                            manager_response.send_getting_started_message(sender_id, user.first_name)
                        )
                        response_msg.append(
                            manager_response.send_getting_started_message_2(sender_id)
                        )

                        # Set the user in tutorial context
                        context_manager.update_context(sender_id, ContextType.TUTORIAL_ADD_TEAM)

                    # SEARCH HIGHLIGHT SETTING POSTBACK
                    elif postback == 'search_highlights':
                        logger.log_for_user("SEARCH HIGHLIGHTS POSTBACK", sender_id, extra={
                            'action': 'search'
                        })
                        metric_tags.append('action:search')

                        response_msg.append(
                            view_message_helper.search_highlights(sender_id)
                        )

                    # SUBSCRIPTION SETTING POSTBACK
                    elif postback == 'my_subscriptions':
                        logger.log_for_user("SUBSCRIPTION SETTING POSTBACK", sender_id, extra={
                            'action': 'subscriptions'
                        })
                        metric_tags.append('action:see_subscriptions')

                        response_msg.append(
                            view_message_helper.send_subscriptions_settings(sender_id)
                        )

                    # SHARE POSTBACK
                    elif postback == 'share':
                        logger.log_for_user("SHARE POSTBACK", sender_id, extra={
                            'action': 'share'
                        })
                        metric_tags.append('action:share')

                        response_msg.append(
                            manager_share.send_share_introduction_message(sender_id)
                        )
                        response_msg.append(
                            manager_share.send_share_message(sender_id)
                        )

                    # SEE RESULT SETTING POSTBACK
                    elif postback == 'see_result_setting':
                        logger.log_for_user("SEE RESULT SETTING POSTBACK", sender_id, extra={
                            'action': 'settings'
                        })
                        metric_tags.append('action:see_result_setting')

                        response_msg.append(
                            view_message_helper.send_send_see_result_settings(sender_id)
                        )

                # Send the metrics about user interaction
                metrics.send_metric("user.action.message", tags=metric_tags)

                # Log the responses
                for msg in response_msg:
                    logger.log_for_user("Message sent", sender_id, extra={
                        'full_msg': msg,
                        'msg_type': 'response'
                    })
                HighlightsBotView.LATEST_SENDER_ID = 0

        if not env.DEBUG:
            return HttpResponse()

        else:
            # DEBUG MODE ONLY
            formatted_response = "[" + ", ".join(response_msg) + "]"
            return JsonResponse(formatted_response, safe=False)


class HighlightView(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        type = kwargs.get('type')
        extended = type == 'extended'

        if type is not None and not extended:
            # go to the url without the extended option
            return redirect(request.get_full_path().replace('/' + type, ''))

        if request.GET.get('user_id'):
            user_id = int(request.GET.get('user_id'))

            # regex selecting everything before the parameters in the url
            regex = '(^.*?)\?'
            path_no_params = re.compile(regex, 0).search(request.get_full_path()).groups()[0]

            response = redirect(path_no_params)

            # place user_id in a cookie
            response.set_cookie('user_id', user_id)

            # go to the url without the tracking id
            return response

        user_id = request.COOKIES.get('user_id') if request.COOKIES.get('user_id') else 0

        is_recommendation = request.GET.get('recommendation')
        highlight_models = latest_highlight_manager.get_highlights_by_id(id)

        # user tracking recording if user clicked on link
        user_manager.increment_user_highlight_click_count(user_id)
        metrics.send_metric("user.action.highlight_view", tags=[
            'highlight-type:{}'.format('extended' if extended else 'normal'),
            'recommendation:{}'.format('true' if is_recommendation else 'false'),
            'valid:{}'.format('true' if highlight_models else 'false')
        ])

        if not highlight_models:
            return HttpResponseBadRequest('<h1>Invalid link</h1>')

        if is_recommendation:
            recommendation_manager.add_recommendation(user_id, highlight_models[0])

        highlight_to_send = latest_highlight_manager.get_best_highlight(highlight_models, extended=extended)

        # Link click tracking
        latest_highlight_manager.increment_click_count(highlight_to_send)

        # Highlights event tracking
        highlight_stat_manager.add_highlight_stat(user_id, highlight_to_send, extended=extended)
        highlight_notification_stat_manager.update_notification_opened(user_id, highlight_to_send)

        # Display page or redirect
        acceptable_providers = [
            providers.DAILYMOTION,
            providers.STREAMABLE,
            providers.MATCHAT_ONLINE,
            providers.CONTENT_VENTURES,
            providers.OK_RU,
            providers.VIDEO_STREAMLET,
            providers.VEUCLIPS,
            providers.VIUCLIPS,
            providers.VIDSTREAM,
            providers.TOCLIPIT,
            providers.CLIPVENTURES,
            providers.TO_STREAMIT,
            providers.UPCLIPS,
            providers.VIDSFORU,
            providers.VSTREAMEU,
            providers.FORSTREAM,
            providers.MYVIDONLINE,
        ]

        # recommendations
        recommendations = recommendation_engine.get_recommendations(highlight_to_send, user_id)
        recommendations = [
            [
                create_link(r['id'], recommendation=True),
                r['img_link'],
                r['team1'].title() + ' - ' + r['team2'].title(),
                r['match_time'].strftime('%A %d %B')
            ]
            for r in recommendations
        ]

        logger.log_for_user('Recommendations for user ' + str(user_id), user_id, extra={
            'recommendations': recommendations
        })

        if [p for p in acceptable_providers if p in highlight_to_send.link]:

            return TemplateResponse(request, 'highlight.html', {
                'title': highlight_to_send.get_match_name_no_result(),
                'link': highlight_to_send.link,
                'img_link': highlight_to_send.img_link,
                'recommendations': recommendations
            })

        else:
            return redirect(highlight_to_send.link)
