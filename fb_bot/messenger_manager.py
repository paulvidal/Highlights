import json
import random
from collections import OrderedDict
from urllib.parse import quote

import highlights.settings
from fb_bot import client, registration_suggestions
from fb_bot.logger import logger
from fb_bot.messages import *
from fb_bot.model_managers import latest_highlight_manager, football_team_manager, new_football_registration_manager, \
    registration_team_manager, registration_competition_manager
from highlights import settings

CLIENT = client.Client()

ACCESS_TOKEN = highlights.settings.get_env_var('MESSENGER_ACCESS_TOKEN')

### MESSAGES ###

def send_help_message(fb_id):
    return send_facebook_message(fb_id, create_message(HELP_MESSAGE))


def send_thank_you_message(fb_id):
    return send_facebook_message(fb_id, create_message(THANK_YOU))


def send_cancel_message(fb_id):
    return send_facebook_message(fb_id, create_message(CANCEL_MESSAGE))


def send_done_message(fb_id):
    return send_facebook_message(fb_id, create_message(DONE_MESSAGE))


def send_search_highlights_message(fb_id):
    return send_facebook_message(fb_id, create_message(SEARCH_HIGHLIGHTS_MESSAGE))


def send_notification_message(fb_id, teams, competitions):
    formatted_registrations = ""
    quick_reply_buttons = [ADD_REGISTRATION_BUTTON, REMOVE_REGISTRATION_BUTTON, DONE_REGISTRATION_BUTTON]

    if len(teams) == 0 and len(competitions) == 0:
        formatted_registrations = NO_REGISTRATION_MESSAGE
        quick_reply_buttons.remove(REMOVE_REGISTRATION_BUTTON)

    # Show teams registered
    for i in range(len(teams)):
        if i > 0:
            formatted_registrations += "\n"

        formatted_registrations += "-> {}".format(teams[i])

    # Separate team and competition sections
    if len(teams) > 0 and len(competitions) > 0:
        formatted_registrations += "\n\n"

    # Show competitions registered
    for i in range(len(competitions)):
        if i > 0:
            formatted_registrations += "\n"

        formatted_registrations += "-> {}".format(competitions[i])

    return send_facebook_message(
        fb_id, create_quick_text_reply_message(SUBSCRIPTION_MESSAGE.format(formatted_registrations), quick_reply_buttons))


def send_add_registration_message(fb_id, suggestions_override=None):
    registrations = registration_team_manager.get_teams_for_user(fb_id) \
                    + registration_competition_manager.get_competitions_for_user(fb_id)

    suggestions = registration_suggestions.get_suggestion_for_registrations(registrations) if not suggestions_override else suggestions_override
    suggestions = [s.title() for s in suggestions]

    return send_facebook_message(fb_id, create_quick_text_reply_message(ADD_REGISTRATIONS_MESSAGE, suggestions))


def send_delete_registration_message(fb_id, registrations):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_REGISTRATION_MESSAGE, registrations[:10] + [CANCEL_BUTTON]))


def send_recommended_registration_message(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_RECOMMEND_MESSAGE, recommended[:9] + [OTHER_BUTTON, CANCEL_BUTTON]))


def send_registration_not_found_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_NOT_FOUND_MESSAGE, [TRY_AGAIN_BUTTON, CANCEL_BUTTON]))


def send_registration_added_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(REGISTRATION_ADDED_MESSAGE.format(team)))


def send_registration_to_delete_not_found_message(fb_id, registrations):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_REGISTRATION_NOT_FOUND_MESSAGE, registrations + [CANCEL_BUTTON]))


def send_registration_deleted_message(fb_id, teams):
    return send_facebook_message(fb_id, create_message(REGISTRATION_DELETED_MESSAGE.format(teams)))


def send_getting_started_message(fb_id, user_name):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE.format(user_name)))


def send_getting_started_message_2(fb_id):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE_2))


def send_error_message(fb_id):
    return send_facebook_message(fb_id, create_message(ERROR_MESSAGE))


def send_highlight_message_for_team(fb_id, team):
    return send_facebook_message(fb_id, get_highlights_for_team(fb_id, team))


# For TUTORIAL

def send_tutorial_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(TUTORIAL_MESSAGE.format(team)))


def send_recommended_team_tutorial_message(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_RECOMMEND_MESSAGE, recommended[:9] + [OTHER_BUTTON]))


def send_team_not_found_tutorial_message(fb_id):
    return send_facebook_message(fb_id, create_message(REGISTRATION_NOT_FOUND_MESSAGE))


# FIXME: duplication with real search
def send_tutorial_highlight(fb_id, team):
    highlights = latest_highlight_manager.get_highlights_for_team(team)

    if highlights == []:
        # Case no highlight found for the team, use example such as PSG, Barcelona, Real Madrid
        highlights = latest_highlight_manager.get_highlights_for_team('psg') \
                     + latest_highlight_manager.get_highlights_for_team('barcelona') \
                     + latest_highlight_manager.get_highlights_for_team('real madrid')

    # Eliminate duplicates
    highlights = latest_highlight_manager.get_unique_highlights(highlights)

    # Order highlights by date and take the first one
    highlight = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)[0]

    return send_facebook_message(fb_id, create_generic_attachment(highlights_to_json(fb_id, [highlight])))


# For scheduler
def send_highlight_messages(fb_ids, highlight_models):
    attachments = [create_generic_attachment(highlights_to_json(fb_id, highlight_models)) for fb_id in fb_ids]
    return send_batch_multiple_facebook_messages(fb_ids, attachments)


def send_highlight_won_introduction_message(fb_ids, highlight_model):

    if highlight_model.category.name == "champions league" and highlight_model.score1 + highlight_model.score2 >= 5:
        # CHAMPIONS LEAGUE LOT OF GOALS MESSAGE
        message = random.choice(NEW_HIGHLIGHT_CHAMPIONS_LEAGUE_LOT_OF_GOALS_MESSAGES)

    elif highlight_model.category.name == "champions league":
        # CHAMPIONS LEAGUE MESSAGE
        message = random.choice(NEW_HIGHLIGHT_CHAMPIONS_LEAGUE_MESSAGES)

    elif highlight_model.score1 + highlight_model.score2 >= 5:
        # LOT OF GOALS MESSAGE
        message = random.choice(NEW_HIGHLIGHT_LOT_OF_GOALS_MESSAGES).format(highlight_model.category.name.title())

    else:
        # NORMAL MESSAGE
        message = random.choice(NEW_HIGHLIGHT_MESSAGES).format(highlight_model.category.name.title())

    return send_batch_facebook_message(fb_ids, create_message(message))


def send_highlight_draw_introduction_message(fb_ids, highlight_model):
    # DRAW MESSAGE
    message = random.choice(NEW_HIGHLIGHT_DRAW_MATCH).format(highlight_model.category.name.title())

    return send_batch_facebook_message(fb_ids, create_message(message))


def send_highlight_lost_introduction_message(fb_ids, highlight_model):
    # LOSE MESSAGE
    message = random.choice(NEW_HIGHLIGHT_LOST_MATCH).format(highlight_model.category.name.title())

    return send_batch_facebook_message(fb_ids, create_message(message))


def send_score(fb_ids, highlight_model):
    goal_data = highlight_model.goal_data

    # Do not send a message if no goal data
    if not goal_data:
        return

    team1_goals = [goal for goal in goal_data if goal['team'] == 1]
    team2_goals = [goal for goal in goal_data if goal['team'] == 2]

    goals_message = _format_goals_message(highlight_model.team1.name.title(),
                                         team1_goals,
                                         highlight_model.team2.name.title(),
                                         team2_goals)

    return send_batch_facebook_message(fb_ids, create_message(goals_message))


def _format_goals_message(team1, team1_goals, team2, team2_goals):
    formatted_team1_goals = _format_team_goals(team1_goals)
    formatted_team2_goals = _format_team_goals(team2_goals)

    t1 = '{} {}\n{}'.format(team1, EMOJI_FOOTBALL, formatted_team1_goals) if team1_goals else ''
    separator = '\n\n' if team1_goals and team2_goals else ''
    t2 = '{} {}\n{}'.format(team2, EMOJI_FOOTBALL, formatted_team2_goals) if team2_goals else ''

    return t1 + separator + t2


def _format_team_goals(goals_formatted):
    goals = OrderedDict()

    for g in goals_formatted:
        player = g['player']
        time = str(g['elapsed'])

        goal_type = g.get('goal_type')

        # Add goal type indicator
        if goal_type == 'penalty':
            time += ' (p)'
        elif goal_type == 'own goal':
            time += ' (o.g)'

        if not goals.get(player):
            goals[player] = [time]
        else:
            goals.get(player).append(time)

    goals_formatted = [((player[0] + '. ' + ' '.join(player.split()[1:])) if len(player.split()) > 1 else player)
                       + " - {}".format(', '.join(goals[player])) for player in goals]

    return '\n'.join(goals_formatted)


### MAIN METHOD ###

def send_batch_multiple_facebook_messages(fb_ids, messages):
    """
    Send different messages to all fb_id
    """
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msgs = []

    for i in range(len(fb_ids)):
        response_msgs.append(json.dumps(
            {
                "recipient": {
                    "id": str(fb_ids[i])
                },
                "message": messages[i]
            })
        )

    CLIENT.send_fb_messages_async(post_message_url, response_msgs)
    logger.log(response_msgs)

    return response_msgs


def send_batch_facebook_message(fb_ids, message):
    """
    Send same message to all fb_id
    """
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msgs = []

    for i in range(len(fb_ids)):
        response_msgs.append(json.dumps(
            {
                "recipient": {
                    "id": str(fb_ids[i])
                },
                "message": message
            })
        )

    CLIENT.send_fb_messages_async(post_message_url, response_msgs)
    logger.log(response_msgs)

    return response_msgs


def send_facebook_message(fb_id, message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps(
        {
            "recipient": {
                "id": fb_id
            },
            "message": message
        })

    CLIENT.send_fb_message(post_message_url, response_msg)
    logger.log(response_msg)

    return response_msg


def send_typing(fb_id):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps(
        {
            "recipient": {
                "id": fb_id
            },
            "sender_action": "typing_on"
        })

    CLIENT.send_fb_message(post_message_url, response_msg)


#
# Highlights getters
#

def has_highlight_for_team(team):
    return latest_highlight_manager.get_highlights_for_team(team)


# FIXME: code duplicated for tutorial
def get_highlights_for_team(fb_id, team, highlight_count=10):
    highlights = latest_highlight_manager.get_highlights_for_team(team)

    if highlights == []:
        # Case no highlight found for the team
        return create_quick_text_reply_message(NO_HIGHLIGHTS_MESSAGE, [SEARCH_AGAIN_HIGHLIGHTS_BUTTON,
                                                                       HELP_BUTTON,
                                                                       CANCEL_BUTTON])

    if not highlights:
        # Case no team name matched
        similar_team_names = football_team_manager.similar_football_team_names(team)

        # Register wrong search
        new_football_registration_manager.add_football_registration(team, 'user')

        # Check if name of team was not properly written
        if len(similar_team_names) == 0:
            return create_quick_text_reply_message(NO_MATCH_FOUND, [SEARCH_AGAIN_HIGHLIGHTS_BUTTON,
                                                                    HELP_BUTTON,
                                                                    CANCEL_BUTTON])

        elif len(similar_team_names) == 1:
            # Case where only one team is similar, so send the highlights for this team
            # -> error correction as user might have done a typo
            team = similar_team_names[0]
            highlights = latest_highlight_manager.get_highlights_for_team(team)

        elif len(similar_team_names) >= 2:
            similar_team_names = [team_name.title() for team_name in similar_team_names]
            return create_quick_text_reply_message(NO_MATCH_FOUND_TEAM_RECOMMENDATION, similar_team_names[:9]
                                                   + [HELP_BUTTON,
                                                      CANCEL_BUTTON])

    # Eliminate duplicates
    highlights = latest_highlight_manager.get_unique_highlights(highlights)

    # Order highlights by date and take the first 10
    highlights = sorted(highlights, key=lambda h: h.get_parsed_time_since_added(), reverse=True)[:highlight_count]

    return create_generic_attachment(highlights_to_json(fb_id, highlights))


#
# Highlights to json
#


def highlights_to_json(fb_id, highlight_models):
    return list(map(lambda h: highlight_to_json(fb_id, h), highlight_models))


def highlight_to_json(fb_id, highlight_model):
    return {
        "title": highlight_model.get_match_name(),
        "image_url": highlight_model.img_link,
        "subtitle": highlight_model.category.name.title(),
        "default_action": {
            "type": "web_url",
            "url": create_tracking_link(fb_id, highlight_model),
            "messenger_extensions": "false",
            "webview_height_ratio": "full"
        }
    }


# Essential method for link creation and redirection to website (and tracking)
def create_tracking_link(fb_id, highlight_model):
    # Form correct url to redirect to server
    link = settings.BASE_URL + "/highlight?team1={}&score1={}&team2={}&score2={}&date={}&user_id=".format(
        quote(highlight_model.team1.name.lower()),
        highlight_model.score1,
        quote(highlight_model.team2.name.lower()),
        highlight_model.score2,
        highlight_model.get_parsed_time_since_added().date()
    )

    tracking_link = link + str(fb_id)

    return tracking_link


#
# JSON message formatter
#

def create_message(text):
    return {
        "text": text
    }


def create_quick_text_reply_message(text, quick_replies):
    formatted_quick_replies = []

    for quick_reply in quick_replies:
        formatted_quick_replies.append({
            "content_type": "text",
            "title": quick_reply,
            "payload": "NO_PAYLOAD"
        })

    return {
        "text": text,
        "quick_replies": formatted_quick_replies
    }


def create_list_attachement(elements):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "list",
                "top_element_style": "compact",
                "elements": elements
            }
        }
    }


def create_generic_attachment(elements):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
