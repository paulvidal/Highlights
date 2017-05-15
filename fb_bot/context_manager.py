from enum import Enum

from fb_bot.user_manager import get_user


class ContextType(Enum):
    NONE = 0
    MENU = 1
    NOTIFICATIONS_SETTING = 2
    ADDING_TEAM = 3
    DELETING_TEAM = 4


def update_context(fb_id, context):
    if not isinstance(context, ContextType):
        raise TypeError("context should be of type ContextType")

    user = get_user(fb_id)
    user.context = context.value
    user.save()


def is_menu_context(fb_id):
    return get_user(fb_id).context == ContextType.MENU.value


def is_notifications_setting_context(fb_id):
    return get_user(fb_id).context == ContextType.NOTIFICATIONS_SETTING.value


def is_notifications_setting_continue_context(fb_id):
    return get_user(fb_id).context == ContextType.NOTIFICATIONS_SETTING_CONTINUE.value


def is_adding_team_context(fb_id):
    return get_user(fb_id).context == ContextType.ADDING_TEAM.value


def is_deleting_team_context(fb_id):
    return get_user(fb_id).context == ContextType.DELETING_TEAM.value

