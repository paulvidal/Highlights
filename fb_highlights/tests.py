import json

from django.test import TestCase, Client

from fb_bot import scheduler_tasks
from fb_bot.messages import *
from fb_bot.messenger_manager import sender
from fb_bot.model_managers import registration_team_manager, registration_competition_manager, user_manager, \
    latest_highlight_manager
from fb_highlights import tests_helper
from fb_highlights.models import LatestHighlight
from fb_highlights.tests_helper import TIME_40_MINUTES_EARLIER, TIME_NOW, TIME_3_DAYS_EARLIER
from highlights import settings

TEST_USER_ID = 1119096411506599


class MessengerBotTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(MessengerBotTestCase, cls).setUpClass()

        tests_helper.class_setup()
        tests_helper.fill_db(TEST_USER_ID)

    def setUp(self):
        self.client = Client()
        tests_helper.set_up(TEST_USER_ID)

    def send_message(self, sender, message):
        m = json.dumps({
            "object": "page",
            "entry": [
                {
                    "id": "1661818147398143",
                    "time": 1493911374840,
                    "messaging": [
                        {
                            "sender": {
                                "id": str(sender)
                            },
                            "recipient": {
                                "id": "1661818147398143"
                            },
                            "timestamp": 1493911373874,
                            "message": {
                                "mid": "mid.$cAAXnamDTS6JiBVPQMlb1A6Hcns6f",
                                "seq": 255027,
                                "text": str(message)
                            }
                        }
                    ]
                }
            ]
        })

        response = self.client.post('/d08fcf03937a116ab14ea30725c72d33ac715bcfa085e296cd/', m, content_type='application/json')
        return json.loads(response.json())

    # SUBSCRIPTION TESTS

    def test_my_subscriptions(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'subscriptions')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "I am currently sending you the highlights for the following ⚽ subscriptions: \n\n-> No team or competition registered\n\nDo you want to ADD or REMOVE a subscription?",
                    "quick_replies": [
                        {
                            "title": "➕ Add",
                            "content_type": "text",
                            "payload": "NO_PAYLOAD"
                        },
                        {
                            "title": "👌 Done",
                            "content_type": "text",
                            "payload": "NO_PAYLOAD"
                        }
                    ]
                }
            }
        ])

    def test_add_team_subscription(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')

        # When
        json_response = self.send_message(TEST_USER_ID, 'add')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "Tell me the name of the team or competition you want to add 🔥",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Psg"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Arsenal"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Champions League"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Barcelona"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Manchester United"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Europa League"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Bayern Munich"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Real Madrid"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Liverpool"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "I'm good 👍"
                        },
                    ],
                }
            }
        ])

    def test_adding_chelsea(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')
        self.send_message(TEST_USER_ID, 'add')

        # When
        json_response = self.send_message(TEST_USER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "chelsea was successfully registered 👍"
                }
            },
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "Tell me the name of the team or competition you want to add 🔥",
                    "quick_replies": [
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Champions League"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Tottenham"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "England"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Premier League"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Psg"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Arsenal"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Barcelona"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Manchester United"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Europa League"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Bayern Munich"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "I'm good 👍"
                        },
                    ],
                }
            }
        ])

    def test_adding_chelsea_adds_the_team(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')
        self.send_message(TEST_USER_ID, 'add')
        self.send_message(TEST_USER_ID, 'chelsea')

        # When
        json_response = self.send_message(TEST_USER_ID, "I'm good 👍")

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "quick_replies": [
                        {
                            "title": "➕ Add",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "➖ Remove",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "👌 Done",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        }
                    ],
                    "text": "I am currently sending you the highlights for the following ⚽ subscriptions: \n\n-> Chelsea\n\nDo you want to ADD or REMOVE a subscription?"
                }
            }
        ])

    def test_add_multiple_teams_in_a_row(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')
        self.send_message(TEST_USER_ID, 'add')
        self.send_message(TEST_USER_ID, 'chelsea')
        self.send_message(TEST_USER_ID, 'barcelona')

        # When
        json_response = self.send_message(TEST_USER_ID, "I'm good 👍")

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "quick_replies": [
                        {
                            "title": "➕ Add",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "➖ Remove",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "👌 Done",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        }
                    ],
                    "text": "I am currently sending you the highlights for the following ⚽ subscriptions: \n\n-> Barcelona\n-> Chelsea\n\nDo you want to ADD or REMOVE a subscription?"
                }
            }
        ])

    def test_remove_team(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')
        self.send_message(TEST_USER_ID, 'add')
        self.send_message(TEST_USER_ID, 'chelsea')
        self.send_message(TEST_USER_ID, "I'm good 👍")

        # When
        json_response = self.send_message(TEST_USER_ID, 'remove')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "quick_replies": [
                        {
                            "title": "Chelsea",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "❌ Cancel",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        }
                    ],
                    "text": "Which team or competition do you want to remove?"
                }
            }
        ])

    def test_removing_chelsea(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')
        self.send_message(TEST_USER_ID, 'add')
        self.send_message(TEST_USER_ID, 'chelsea')
        self.send_message(TEST_USER_ID, "I'm good 👍")
        self.send_message(TEST_USER_ID, 'remove')

        # When
        json_response = self.send_message(TEST_USER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "chelsea successfully removed from your subscriptions 👍"
                }
            },
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "quick_replies": [
                        {
                            "title": "➕ Add",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "👌 Done",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        }
                    ],
                    "text": "I am currently sending you the highlights for the following ⚽ subscriptions: \n\n-> No team or competition registered\n\nDo you want to ADD or REMOVE a subscription?"
                }
            }
        ])

    # SEARCH TESTS

    def test_search_is_default(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League',
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=extended&user_id=' + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        },
                        'type': 'template'
                    }
                }
            }
        ])

    def test_search(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'search')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "text": "Tell me for which team or competition should I give you highlight videos? 📺"
                }
            }
        ])

    def test_search_chelsea(self):
        # Given
        self.send_message(TEST_USER_ID, 'search')

        # When
        json_response = self.send_message(TEST_USER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League',
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=extended&user_id=' + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        },
                        'type': 'template'
                    }
                }
            }
        ])

    def test_search_chelsea_with_typo(self):
        # Given
        self.send_message(TEST_USER_ID, 'search')

        # When
        json_response = self.send_message(TEST_USER_ID, 'chelseo')

        # Then
        self.assertEqual(json_response, [
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League',
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=extended&user_id=' + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        },
                        'type': 'template'
                    }
                }
            }
        ])

    def test_search_does_not_show_highlights_with_incomplete_data(self):
        # Given
        self.send_message(TEST_USER_ID, 'search')

        # When
        json_response = self.send_message(TEST_USER_ID, 'marseille')

        # Then
        self.assertNotEqual(json_response, [
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    "title": "Marseille -1 - -1 Monaco",
                                    "subtitle": "Ligue 1",
                                    "image_url": "http://sportyhl/images?marseille-monaco",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=marseille&score1=-1&team2=monaco&score2=-1&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=marseille&score1=-1&team2=monaco&score2=-1&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight"
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=marseille&score1=-1&team2=monaco&score2=-1&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight"
                                        }
                                    ]
                                }
                            ]
                        },
                        'type': 'template'
                    }
                }
            }
        ])

    def test_change_see_result_setting(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'spoiler')

        # Then
        self.assertEqual(json_response, [{
            'recipient': {
                'id': str(TEST_USER_ID)
            },
            "messaging_type": "RESPONSE",
            'message': {
                'text': 'Do you want to receive match results/spoiler (score, goal scorers...) along with your highlight messages, or hide them?\n\nCurrently: Showing results',
                'quick_replies': [
                    {
                        'content_type': 'text',
                        'payload': 'NO_PAYLOAD',
                        'title': 'Show'
                    },
                    {
                        'content_type': 'text',
                        'payload': 'NO_PAYLOAD',
                        'title': 'Hide'
                    },
                    {
                        'content_type': 'text',
                        'payload': 'NO_PAYLOAD',
                        'title': '❌ Cancel'
                    }
                ]
            }
        }])

    def test_change_see_result_setting_to_hide_result(self):
        # Given
        self.send_message(TEST_USER_ID, 'see result setting')

        # When
        json_response = self.send_message(TEST_USER_ID, HIDE_BUTTON)

        # Then
        self.assertEqual(json_response, [{
            'recipient': {
                'id': str(TEST_USER_ID)
            },
            "messaging_type": "RESPONSE",
            'message': {
                'text': "Setting successfully changed 👍"
            }
        }])

    def test_change_see_result_setting_to_hide_result_changes_permanently(self):
        # Given
        self.send_message(TEST_USER_ID, 'see result setting')
        self.send_message(TEST_USER_ID, HIDE_BUTTON)

        # When
        json_response = self.send_message(TEST_USER_ID, 'see result setting')

        # Then
        self.assertEqual(json_response, [{
            'recipient': {
                'id': str(TEST_USER_ID)
            },
            "messaging_type": "RESPONSE",
            'message': {
                'text': 'Do you want to receive match results/spoiler (score, goal scorers...) along with your highlight messages, or hide them?\n\nCurrently: Hiding results',
                'quick_replies': [
                    {
                        'content_type': 'text',
                        'payload': 'NO_PAYLOAD',
                        'title': 'Show'
                    },
                    {
                        'content_type': 'text',
                        'payload': 'NO_PAYLOAD',
                        'title': 'Hide'
                    },
                    {
                        'content_type': 'text',
                        'payload': 'NO_PAYLOAD',
                        'title': '❌ Cancel'
                    }
                ]
            }
        }])

        # Set back to default state
        self.send_message(TEST_USER_ID, CANCEL_BUTTON)

    def test_search_see_result_hidden(self):
        # Given
        user = user_manager.get_user(TEST_USER_ID)
        user.see_result = False
        user.save()

        # When
        json_response = self.send_message(TEST_USER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'title': 'Chelsea - Barcelona',
                                    'subtitle': 'Champions League',
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(
                                            TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(
                                                TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=extended&user_id=' + str(
                                                TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        },
                        'type': 'template'
                    }
                }
            }
        ])

        # Set back old properties
        user.see_result = True
        user.save()

    def test_search_does_not_show_not_sent_result(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'tottenham')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
                "messaging_type": "RESPONSE",
                "message": {
                    "quick_replies": [
                        {
                            "title": "🔍 Search again",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "❓ Help",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        },
                        {
                            "title": "❌ Cancel",
                            "payload": "NO_PAYLOAD",
                            "content_type": "text"
                        }
                    ],
                    "text": "I'm so sorry but I could not find any recent highlight video for your team or competition 💔"
                }
            }
        ])

    def test_share(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'share')

        # Then
        self.assertEqual(json_response, [{
            'recipient': {
                'id': str(TEST_USER_ID)
            },
            "messaging_type": "RESPONSE",
            'message': {
                'text': "I'm counting on you to make me grow! 💪"
            }
        }, {
            'recipient': {
                'id': str(TEST_USER_ID)
            },
            "messaging_type": "RESPONSE",
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [{
                            "title": "Start a conversation with me!",
                            "subtitle": "I will send you the highlight videos for your teams as soon as matches occur.",
                            "image_url": settings.BASE_URL + "/static/images/share.png",
                            "buttons": [
                                {
                                    "type": "element_share",
                                    "share_contents": {
                                        "attachment": {
                                            "type": "template",
                                            "payload": {
                                                "template_type": "generic",
                                                "elements": [{
                                                    "title": "Start a conversation with me!",
                                                    "subtitle": "I will send you the highlight videos for your teams as soon as matches occur.",
                                                    "image_url": settings.BASE_URL + "/static/images/share.png",
                                                    "default_action": {
                                                        "type": "web_url",
                                                        "url": "https://m.me/highlightsSportBot/"
                                                    },
                                                    "buttons": [
                                                        {
                                                            "type": "web_url",
                                                            "url": "https://m.me/highlightsSportBot/",
                                                            "title": "Start " + EMOJI_HEART
                                                        }
                                                    ]
                                                }]
                                            }
                                        }
                                    }
                                }
                            ]
                        }]
                    }
                }
            }
        }])

        # Set back to default state
        self.send_message(TEST_USER_ID, CANCEL_BUTTON)


class FetcherTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(FetcherTestCase, cls).setUpClass()

        tests_helper.class_setup()
        tests_helper.fill_db(TEST_USER_ID)

    def setUp(self):
        self.client = Client()
        tests_helper.set_up(TEST_USER_ID)

    def fetch_highlights(self):
        scheduler_tasks.fetch_highlights('test')

    def test_highlight_inverted_home_and_away_teams_inserted_swapped_if_more_than_1_matches_different(self):
        # Given

        # When
        self.fetch_highlights()

        # Then
        highlight = [h for h in latest_highlight_manager.get_all_highlights() if h.link == 'http://footyroom/chelsea-barcelona4'][0]

        self.assertEqual(highlight.team1.name, 'chelsea')
        self.assertEqual(highlight.score1, 0)
        self.assertEqual(highlight.team2.name, 'barcelona')
        self.assertEqual(highlight.score2, 2)

    def test_highlight_inverted_home_and_away_teams_inserted_not_swapped_if_only_one_other_match(self):
        # Given

        # When
        self.fetch_highlights()

        # Then
        highlight = [h for h in latest_highlight_manager.get_all_highlights() if h.link == 'http://hoofoot/arsenal-liverpool2'][0]

        self.assertEqual(highlight.team1.name, 'liverpool')
        self.assertEqual(highlight.score1, 4)
        self.assertEqual(highlight.team2.name, 'arsenal')
        self.assertEqual(highlight.score2, 0)

    def test_highlight_inverted_home_and_away_teams_inserted_swapped_if_already_sent_highlight(self):
        # Given

        # When
        self.fetch_highlights()

        # Then
        highlight = [h for h in latest_highlight_manager.get_all_highlights() if h.link == 'http://hoofoot/swansea-arsenal2'][0]

        self.assertEqual(highlight.team1.name, 'swansea')
        self.assertEqual(highlight.score1, 4)
        self.assertEqual(highlight.team2.name, 'arsenal')
        self.assertEqual(highlight.score2, 0)


class SchedulerTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(SchedulerTestCase, cls).setUpClass()

        tests_helper.class_setup()
        tests_helper.fill_db(TEST_USER_ID)

        # Add test registrations
        registration_team_manager.add_team(TEST_USER_ID, "barcelona")
        registration_competition_manager.add_competition(TEST_USER_ID, "premier league")
        registration_competition_manager.add_competition(TEST_USER_ID, "ligue 1")
        registration_competition_manager.add_competition(TEST_USER_ID, "europa league")

    def setUp(self):
        self.client = Client()
        tests_helper.set_up(TEST_USER_ID)

    def send_most_recent_highlights(self):
        scheduler_tasks.send_most_recent_highlights()

    def test_scheduler_send_highlight_message_for_subscribed_team(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn(
            {
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
                                    "title": "Burnley 0 - 2 Barcelona",
                                    "subtitle": "Champions League",
                                    "image_url": "http://hoofoot/images?burnley-barcelona",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=burnley&score1=0&team2=barcelona&score2=2&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=burnley&score1=0&team2=barcelona&score2=2&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=burnley&score1=0&team2=barcelona&score2=2&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_scheduler_does_not_send_highlight_message_for_subscribed_team_when_too_recent(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertNotIn({
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
                                "title": "Barcelona 1 - 1 Liverpool",
                                "subtitle": "Champions League",
                                "image_url": "http://hoofoot/images?barcelona-liverpool",
                                "default_action": {
                                    "type": "web_url",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full",
                                    "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(TIME_NOW.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(TIME_NOW.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                        "title": "Short highlight",
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(TIME_NOW.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                        "title": "Extended highlight",
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }, messages)

    def test_scheduler_sends_highlight_message_for_subscribed_team_when_too_recent_but_priority_is_set(self):
        # Given
        h = LatestHighlight.objects.filter(link='http://hoofoot/barcelona-liverpool')[0]
        h.priority_short = 1
        h.save()

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn({
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
                                "title": "Barcelona 1 - 1 Liverpool",
                                "subtitle": "Champions League",
                                "image_url": "http://hoofoot/images?barcelona-liverpool",
                                "default_action": {
                                    "type": "web_url",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full",
                                    "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(TIME_NOW.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(TIME_NOW.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                        "title": "Short highlight",
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(TIME_NOW.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                        "title": "Extended highlight",
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }, messages)

        # Set back old properties
        h.priority_short = 0
        h.save()

    def test_scheduler_send_highlight_message_for_subscribed_competition(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn(
            {
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
                                    "title": "Arsenal 0 - 4 Liverpool",
                                    "subtitle": "Premier League",
                                    "image_url": "http://hoofoot/images?arsenal-liverpool",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            },
            messages)

    def test_scheduler_send_highlight_goals(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn(
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "MESSAGE_TAG",
                "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
                "message": {
                    "text": "Barcelona ⚽\nL. Messi - 4 (p), 90\nL. Suarez - 43\n\nReal Madrid ⚽\nC. Ronaldo - 10\nG. Pique - 56 (o.g)"
                }
            },
            messages)

    def test_scheduler_send_highlight_goals_only_1_team_scored(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn(
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "MESSAGE_TAG",
                "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
                "message": {
                    "text": "Arsenal ⚽\nO. Giroud - 15"
                }
            },
            messages)

    def test_scheduler_send_highlight_with_see_result_disabled(self):
        # Given
        user = user_manager.get_user(TEST_USER_ID)
        user.see_result = False
        user.save()

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn(
            {
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
                                    'title': 'Burnley - Barcelona',
                                    'subtitle': 'Champions League',
                                    'image_url': 'http://hoofoot/images?burnley-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=burnley&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=burnley&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=burnley&score1=0&team2=barcelona&score2=2&date=' + str(TIME_40_MINUTES_EARLIER.date()) + '&type=extended&user_id=' + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

        self.assertNotIn(
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "messaging_type": "MESSAGE_TAG",
                "tag": "NON_PROMOTIONAL_SUBSCRIPTION",
                "message": {
                    "text": "Barcelona ⚽\nL. Messi - 4 (p), 90\nL. Suarez - 43\n\nReal Madrid ⚽\nC. Ronaldo - 10\nG. Pique - 56 (o.g)"
                }
            },
            messages)

        # Set back old properties
        user.see_result = True
        user.save()

    def test_scheduler_does_not_send_highlight_if_highlight_for_same_match_already_sent(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertNotIn(
            {
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
                                    "title": "Chelsea 0 - 2 Barcelona",
                                    "subtitle": "Champions League",
                                    "image_url": "http://hoofoot/images?chelsea-barcelona2",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_scheduler_does_not_send_highlight_if_highlight_inverted_home_and_away_teams(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertNotIn(
            {
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
                                    "title": "Barcelona 2 - 0 Chelsea",
                                    "subtitle": "Champions League",
                                    "image_url": "http://hoofoot/images?chelsea-barcelona3",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=2&team2=chelsea&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=barcelona&score1=2&team2=chelsea&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=barcelona&score1=2&team2=chelsea&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight",
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_scheduler_overrides_picture_and_goals_for_highlights(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertIn(
            {
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
                                    "title": "Manchester City 0 - 0 Tottenham",
                                    "subtitle": "Premier League",
                                    "image_url": "http://footyroom/images?manchester_city-tottenham",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=manchester%20city&score1=0&team2=tottenham&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=manchester%20city&score1=0&team2=tottenham&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight"
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=manchester%20city&score1=0&team2=tottenham&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_scheduler_does_not_send_highlight_with_incomplete_data(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertNotIn(
            {
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
                                    "title": "Marseille -1 - -1 Monaco",
                                    "subtitle": "Ligue 1",
                                    "image_url": "http://sportyhl/images?marseille-monaco",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=marseille&score1=-1&team2=monaco&score2=-1&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=marseille&score1=-1&team2=monaco&score2=-1&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight"
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=marseille&score1=-1&team2=monaco&score2=-1&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_scheduler_does_not_send_highlight_when_date_too_old(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertNotIn(
            {
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
                                    "title": "Swansea 0 - 3 Barcelona",
                                    "subtitle": "Champions League",
                                    "image_url": "http://footyroom/images?swansea-barcelona",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=swansea&score1=0&team2=barcelona&score2=3&date=" + str(TIME_3_DAYS_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=swansea&score1=0&team2=barcelona&score2=3&date=" + str(TIME_3_DAYS_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight"
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=swansea&score1=0&team2=barcelona&score2=3&date=" + str(TIME_3_DAYS_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_do_not_send_champions_league(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        self.assertNotIn(
            {
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
                                    "title": "Swansea 2 - 0 Liverpool",
                                    "subtitle": "Europa League",
                                    "image_url": "http://hoofoot/images?swansea-liverpool",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=swansea&score1=2&team2=liverpool&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=swansea&score1=2&team2=liverpool&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight"
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=swansea&score1=2&team2=liverpool&score2=0&date=" + str(TIME_40_MINUTES_EARLIER.date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
                                            "title": "Extended highlight"
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                }
            }, messages)
