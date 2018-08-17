from fb_bot import registration_suggestions
from fb_bot.messages import *
from fb_bot.messenger_manager.formatter import create_message, create_quick_text_reply_message
from fb_bot.messenger_manager.sender import send_facebook_message
from fb_bot.model_managers import registration_team_manager, registration_competition_manager, user_manager


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

    return send_facebook_message(fb_id, create_quick_text_reply_message(ADD_REGISTRATIONS_MESSAGE, suggestions + [I_M_GOOD_BUTTON]))


def send_delete_registration_message(fb_id, registrations):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_REGISTRATION_MESSAGE, registrations[:10] + [CANCEL_BUTTON]))


def send_recommended_registration_message(fb_id, recommended):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_RECOMMEND_MESSAGE, recommended[:9] + [OTHER_BUTTON, CANCEL_BUTTON]))


def send_registration_not_found_message(fb_id):
    return send_facebook_message(fb_id, create_quick_text_reply_message(REGISTRATION_NOT_FOUND_MESSAGE, [TRY_AGAIN_BUTTON, I_M_GOOD_BUTTON]))


def send_registration_added_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(REGISTRATION_ADDED_MESSAGE.format(team)))


def send_registration_to_delete_not_found_message(fb_id, registrations):
    return send_facebook_message(fb_id, create_quick_text_reply_message(DELETE_REGISTRATION_NOT_FOUND_MESSAGE, registrations + [CANCEL_BUTTON]))


def send_registration_deleted_message(fb_id, team):
    return send_facebook_message(fb_id, create_message(REGISTRATION_DELETED_MESSAGE.format(team)))


def send_getting_started_message(fb_id, user_name):
    return send_facebook_message(fb_id, create_message(GET_STARTED_MESSAGE.format(user_name)))


def send_getting_started_message_2(fb_id):
    suggestions = registration_suggestions.get_default_suggestion_for_registration()
    suggestions = [s.title() for s in suggestions]

    return send_facebook_message(fb_id, create_quick_text_reply_message(GET_STARTED_MESSAGE_2, suggestions))


def send_error_message(fb_id):
    return send_facebook_message(fb_id, create_message(ERROR_MESSAGE))


def send_see_result_setting(fb_id):
    see_result_setting_value = user_manager.get_see_result_setting(fb_id)
    see_result_setting_value = SEE_RESULT_YES if see_result_setting_value else SEE_RESULT_NO

    return send_facebook_message(fb_id, create_quick_text_reply_message(SEE_RESULT_SETTING_MESSAGE.format(see_result_setting_value),
                                                                        [SHOW_BUTTON, HIDE_BUTTON, CANCEL_BUTTON]))


def send_setting_invalid(fb_id):
    return send_facebook_message(fb_id, create_message(SETTING_INVALID_MESSAGE))


def send_setting_changed(fb_id):
    return send_facebook_message(fb_id, create_message(SETTING_CHANGED_MESSAGE))