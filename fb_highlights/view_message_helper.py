from fb_bot import messenger_manager
from fb_bot.model_managers import context_manager, registration_team_manager, registration_competition_manager
from fb_bot.model_managers.context_manager import ContextType


def search_highlights(sender_id):
    context_manager.update_context(sender_id, ContextType.SEARCH_HIGHLIGHTS)

    return messenger_manager.send_search_highlights_message(sender_id)


def send_subscriptions_settings(sender_id):
    context_manager.update_context(sender_id, ContextType.SUBSCRIPTIONS_SETTING)

    teams = get_teams_formatted(sender_id)
    competitions = get_competitions_formatted(sender_id)

    return messenger_manager.send_notification_message(sender_id, teams, competitions)


def send_send_see_result_settings(sender_id):
    context_manager.update_context(sender_id, ContextType.SETTING_SEE_RESULT)

    return messenger_manager.send_see_result_setting(sender_id)


def get_registrations_formatted(sender_id):
    return get_teams_formatted(sender_id) + get_competitions_formatted(sender_id)


def get_teams_formatted(sender_id):
    teams = registration_team_manager.get_teams_for_user(sender_id)
    return [team.title() for team in teams]


def get_competitions_formatted(sender_id):
    competitions = registration_competition_manager.get_competitions_for_user(sender_id)
    return [competition.title() for competition in competitions]


def accepted_messages(message, accepted_words):
    for words in accepted_words:
        if words in message:
            return True

    return False