from fb_highlights.tests.utils.helper import TEST_USER_ID
from urllib.parse import quote


def create_formatted_highlight_response(team1, score1, team2, score2, competition, image_url, time, score_hidden=False):

    title = '{}{} - {}{}'.format(
        team1,
        ' ' + str(score1) if not score_hidden else '',
        str(score2) + ' ' if not score_hidden else '',
        team2
    )

    url_start = "http://localhost:8000/highlight?team1={}&score1={}&team2={}&score2={}&date=".format(
        quote(team1.lower()),
        score1,
        quote(team2.lower()),
        score2
    )

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
                                    "url": url_start + str(time.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": url_start + str(time.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                        "title": "Short highlight",
                                    },
                                    {
                                        "type": "web_url",
                                        "url": url_start + str(time.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                        "title": "Extended highlight",
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }