from fb_bot import messenger_manager
from fb_bot.model_managers import context_manager, team_manager
from fb_bot.model_managers.context_manager import ContextType


def search_highlights(sender_id):
    context_manager.update_context(sender_id, ContextType.SEARCH_HIGHLIGHTS)

    return messenger_manager.send_search_highlights_message(sender_id)


def send_notification_settings(sender_id):
    context_manager.update_context(sender_id, ContextType.NOTIFICATIONS_SETTING)

    teams = team_manager.get_teams_for_user(sender_id)
    # Format team names
    teams = [team.title() for team in teams]

    return messenger_manager.send_notification_message(sender_id, teams)