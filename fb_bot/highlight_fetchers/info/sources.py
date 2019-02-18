FOOTYROOM = 'footyroom'
FOOTYROOM_VIDEOS = 'footyroom_video'
HOOFOOT = 'hoofoot'
SPORTYHL = 'sportyhl'
HIGHLIGHTS_FOOTBALL = 'highlightsfootball'
OUR_MATCH = 'ourmatch'
YOUTUBE = 'youtube'
BOT = 'bot'


# Sources ready to be show
def get_available_sources():
    return [
        FOOTYROOM,
        FOOTYROOM_VIDEOS,
        HOOFOOT,
        HIGHLIGHTS_FOOTBALL,
        SPORTYHL,
        YOUTUBE,
        BOT,
        OUR_MATCH
    ]


# Sources with all the information such as scores, goal scorers and image, IN ORDER OF PRIORITY
def get_sources_with_complete_data_in_order_of_priority():
    return [
        OUR_MATCH,
        FOOTYROOM,
        FOOTYROOM_VIDEOS,
        HOOFOOT,
        SPORTYHL,
        HIGHLIGHTS_FOOTBALL
    ]


def get_sources_with_incomplete_data():
    return [
        HOOFOOT,
        SPORTYHL,
        HIGHLIGHTS_FOOTBALL,
        BOT,
        OUR_MATCH,
        YOUTUBE
    ]