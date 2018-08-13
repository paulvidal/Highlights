import random
from collections import OrderedDict

from fb_bot.messages import NEW_HIGHLIGHT_CHAMPIONS_LEAGUE_LOT_OF_GOALS_MESSAGES, \
    NEW_HIGHLIGHT_CHAMPIONS_LEAGUE_MESSAGES, NEW_HIGHLIGHT_LOT_OF_GOALS_MESSAGES, NEW_HIGHLIGHT_MESSAGES, \
    NEW_HIGHLIGHT_DRAW_MATCH, NEW_HIGHLIGHT_LOST_MATCH, NEW_HIGHLIGHT_NEUTRAL_MATCH, EMOJI_FOOTBALL
from fb_bot.messenger_manager.formatter import create_generic_attachment, create_message
from fb_bot.messenger_manager.formatter_highlights import highlights_to_json
from fb_bot.messenger_manager.sender import send_batch_different_facebook_messages, \
    send_batch_facebook_message


def send_highlight_messages(fb_ids, highlight_models, see_result):
    attachments = [create_generic_attachment(highlights_to_json(fb_id, highlight_models, see_result=see_result)) for fb_id in fb_ids]
    return send_batch_different_facebook_messages(fb_ids, attachments)


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


def send_highlight_neutral_introduction_message(fb_ids, highlight_model):
    # NEUTRAL MESSAGE
    message = random.choice(NEW_HIGHLIGHT_NEUTRAL_MATCH).format(highlight_model.category.name.title())

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