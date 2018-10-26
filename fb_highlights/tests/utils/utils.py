from fb_highlights.tests.utils.helper import TEST_USER_ID
from urllib.parse import quote


def create_formatted_highlight_response(id, team1, score1, team2, score2, competition, image_url, time, score_hidden=False):

    title = '{}{} - {}{}'.format(
        team1,
        ' ' + str(score1) if not score_hidden else '',
        str(score2) + ' ' if not score_hidden else '',
        team2
    )

    url_start = "http://localhost:8000/highlight/{}".format(id)

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
                                "image_url": image_url,
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