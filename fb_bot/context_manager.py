from enum import Enum


class ContextType(Enum):
    NONE = 0
    MENU = 1
    NOTIFICATIONS_SETTING = 2
    ADDING_TEAM = 3
    DELETING_TEAM = 4


CONTEXT = {}


def update_context(fb_id, context):
    if not isinstance(context, ContextType):
        raise TypeError("context should be of type ContextType")

    CONTEXT.update({fb_id: context})


def is_menu_context(fb_id):
    return CONTEXT.get(fb_id) == ContextType.MENU


def is_notifications_setting_context(fb_id):
    return CONTEXT.get(fb_id) == ContextType.NOTIFICATIONS_SETTING


def is_notifications_setting_continue_context(fb_id):
    return CONTEXT.get(fb_id) == ContextType.NOTIFICATIONS_SETTING_CONTINUE


def is_adding_team_context(fb_id):
    return CONTEXT.get(fb_id) == ContextType.ADDING_TEAM


def is_deleting_team_context(fb_id):
    return CONTEXT.get(fb_id) == ContextType.DELETING_TEAM
