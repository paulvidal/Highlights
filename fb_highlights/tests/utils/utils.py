from fb_highlights.tests.utils.helper import TEST_USER_ID
from fb_highlights.tests.utils.test_highlights import DEFAULT_TEST_IMAGE

from highlights import settings


def create_formatted_highlight_response(id, team1, score1, team2, score2, competition, score_hidden=False, img_link=DEFAULT_TEST_IMAGE):

    title = '{}{} - {}{}'.format(
        team1,
        ' ' + str(score1) if not score_hidden else '',
        str(score2) + ' ' if not score_hidden else '',
        team2
    )

    url_start = settings.BASE_URL + "/highlight/{}".format(id)

    return {
            'recipient': {
                'id': str(TEST_USER_ID)
            },
            "messaging_type": "MESSAGE_TAG",
            "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": title,
                                "subtitle": competition.title(),
                                "image_url": img_link,
                                "default_action": {
                                    "type": "web_url",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full",
                                    "url": url_start + "?user_id=" + str(TEST_USER_ID)
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": url_start + "?user_id=" + str(TEST_USER_ID),
                                        "title": "Short highlights",
                                    },
                                    {
                                        "type": "web_url",
                                        "url": url_start + '/extended?user_id=' + str(TEST_USER_ID),
                                        "title": "Extended highlights",
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }