from enum import Enum

from fb_bot.model_managers.user_manager import get_user


class ContextType(Enum):
    SUBSCRIPTIONS_SETTING = 1
    ADDING_REGISTRATION = 2
    REMOVE_REGISTRATION = 3
    SEARCH_HIGHLIGHTS = 4

    TUTORIAL_ADD_TEAM = 100

    SETTING_SEE_RESULT = 200


def set_default_context(fb_id):
    update_context(fb_id, ContextType.SEARCH_HIGHLIGHTS)


def update_context(fb_id, context):
    if not isinstance(context, ContextType):
        raise TypeError("context should be of type ContextType")

    user = get_user(fb_id)
    user.context = context.value
    user.save()


def is_notifications_setting_context(fb_id):
    return get_user(fb_id).context == ContextType.SUBSCRIPTIONS_SETTING.value


def is_notifications_setting_continue_context(fb_id):
    return get_user(fb_id).context == ContextType.SUBSCRIPTIONS_SETTING_CONTINUE.value


def is_adding_registration_context(fb_id):
    return get_user(fb_id).context == ContextType.ADDING_REGISTRATION.value


def is_deleting_team_context(fb_id):
    return get_user(fb_id).context == ContextType.REMOVE_REGISTRATION.value


def is_searching_highlights_context(fb_id):
    return get_user(fb_id).context == ContextType.SEARCH_HIGHLIGHTS.value


def is_see_result_setting_context(fb_id):
    return get_user(fb_id).context == ContextType.SETTING_SEE_RESULT.value


# TUTORIAL CONTEXT

def is_tutorial_context(fb_id):
    return get_user(fb_id).context == ContextType.TUTORIAL_ADD_TEAM.value