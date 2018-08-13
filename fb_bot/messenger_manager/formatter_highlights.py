from urllib.parse import quote

from highlights import settings


def highlights_to_json(fb_id, highlight_models, see_result=True):
    return [_highlight_to_json(fb_id, h, see_result) for h in highlight_models]


def _highlight_to_json(fb_id, highlight_model, see_result):
    short_highlight_link = _create_tracking_link(fb_id, highlight_model, extended=False)
    extended_highlight_link = _create_tracking_link(fb_id, highlight_model, extended=True)

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
                "title": "Short highlight",
            },
            {
                "type": "web_url",
                "url": extended_highlight_link,
                "title": "Extended highlight",
            }
        ]
    }


def _create_tracking_link(fb_id, highlight_model, extended=False):
    """
    Essential method for link creation and redirection to website (and tracking)
    """

    # Form correct url to redirect to server
    tracking_link = settings.BASE_URL + "/highlight?team1={}&score1={}&team2={}&score2={}&date={}&type={}&user_id={}".format(
        quote(highlight_model.team1.name.lower()),
        highlight_model.score1,
        quote(highlight_model.team2.name.lower()),
        highlight_model.score2,
        highlight_model.get_parsed_time_since_added().date(),
        'extended' if extended else 'short',
        fb_id
    )

    return tracking_link