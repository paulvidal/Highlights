FOOTYROOM = 'footyroom'
FOOTYROOM_VIDEOS = 'footyroom_video'
HOOFOOT = 'hoofoot'
SPORTYHL = 'sportyhl'
HIGHLIGHTS_FOOTBALL = 'highlightsfootball'
OUR_MATCH = 'ourmatch'
BOT = 'bot'


def get_available_sources():
    return [
        FOOTYROOM,
        FOOTYROOM_VIDEOS,
        HOOFOOT,
        HIGHLIGHTS_FOOTBALL,
        SPORTYHL,
        BOT
    ]


def get_sources_without_image():
    return [
        HOOFOOT,
        SPORTYHL,
        HIGHLIGHTS_FOOTBALL,
        OUR_MATCH,
        BOT
    ]


def get_sources_without_score():
    return [
        SPORTYHL,
        HIGHLIGHTS_FOOTBALL
    ]