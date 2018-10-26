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

    return create_link(highlight_model.id,
                       extended=extended,
                       fb_id=fb_id)


def create_link(id, extended=False, fb_id=None):
    # Form correct url to redirect to server
    tracking_link = settings.BASE_URL + "/highlight/" + str(id)

    if extended:
        tracking_link += '/extended'

    if fb_id:
        tracking_link += '?user_id={}'.format(fb_id)

    return tracking_link
