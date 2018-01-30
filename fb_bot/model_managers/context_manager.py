from enum import Enum

from fb_bot.model_managers.user_manager import get_user


class ContextType(Enum):
    NONE = 0
    NOTIFICATIONS_SETTING = 1
    ADDING_TEAM = 2
    DELETING_TEAM = 3
    SEARCH_HIGHLIGHTS = 4

    TUTORIAL_ADD_TEAM = 100
    TUTORIAL_UNDERSTOOD = 101


def update_context(fb_id, context):
    if not isinstance(context, ContextType):
        raise TypeError("context should be of type ContextType")

    user = get_user(fb_id)
    user.context = context.value
    user.save()


def is_notifications_setting_context(fb_id):
    return get_user(fb_id).context == ContextType.NOTIFICATIONS_SETTING.value


def is_notifications_setting_continue_context(fb_id):
    return get_user(fb_id).context == ContextType.NOTIFICATIONS_SETTING_CONTINUE.value


def is_adding_team_context(fb_id):
    return get_user(fb_id).context == ContextType.ADDING_TEAM.value


def is_deleting_team_context(fb_id):
    return get_user(fb_id).context == ContextType.DELETING_TEAM.value


def is_searching_highlights_context(fb_id):
    return get_user(fb_id).context == ContextType.SEARCH_HIGHLIGHTS.value


# TUTORIAL CONTEXT

def is_tutorial_context(fb_id):
    context = get_user(fb_id).context
    return context == ContextType.TUTORIAL_ADD_TEAM.value or context == ContextType.TUTORIAL_UNDERSTOOD.value


def is_tutorial_add_team_context(fb_id):
    return get_user(fb_id).context == ContextType.TUTORIAL_ADD_TEAM.value


def is_tutorial_understood_context(fb_id):
    return get_user(fb_id).context == ContextType.TUTORIAL_UNDERSTOOD.value