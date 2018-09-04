from urllib.parse import quote

from highlights import settings


def highlights_to_json(fb_id, highlight_models, see_result=True):
    return [_highlight_to_json(fb_id, h, see_result) for h in highlight_models]


def _highlight_to_json(fb_id, highlight_model, see_result):
    short_highlight_link = create_link_from_model(fb_id, highlight_model, extended=False)
    extended_highlight_link = create_link_from_model(fb_id, highlight_model, extended=True)

    return {
        "title": highlight_model.get_match_name() if see_result else highlight_model.get_match_name_no_result(),
        "image_url": highlight_model.img_link,
        "subtitle": highlight_model.category.name.title(),
        "default_action": {
            "type": "web_url",
            "url": short_highlight_link,
            "messenger_extensions": "false",
            "webview_height_ratio": "full"
        },
        "buttons": [
            {
                "type": "web_url",
                "url": short_highlight_link,
                "title": "Short highlights",
            },
            {
                "type": "web_url",
                "url": extended_highlight_link,
                "title": "Extended highlights",
            }
        ]
    }


def create_link_from_model(fb_id, highlight_model, extended=False):
    """
    Essential method for link creation and redirection to website (and tracking)
    """

    return create_link(highlight_model.team1.name,
                       highlight_model.score1,
                       highlight_model.team2.name,
                       highlight_model.score2,
                       highlight_model.get_parsed_time_since_added(),
                       extended=extended,
                       fb_id=fb_id)


def create_link(team1, score1, team2, score2, datetime, extended=False, fb_id=None):
    # Form correct url to redirect to server
    tracking_link = settings.BASE_URL + "/highlight?team1={}&score1={}&team2={}&score2={}&date={}&type={}".format(
        quote(team1.lower()),
        score1,
        quote(team2.lower()),
        score2,
        datetime.date(),
        'extended' if extended else 'short',
    )

    if fb_id:
        tracking_link += '&user_id={}'.format(fb_id)

    return tracking_link
