import json

from django.test import TestCase, Client

from fb_bot.messages import HIDE_BUTTON, CANCEL_BUTTON, EMOJI_HEART
from fb_bot.model_managers import user_manager
from fb_highlights.tests import helper
from fb_highlights.tests.helper import TEST_USER_ID
from fb_highlights.tests.helper import TIME_40_MINUTES_EARLIER
from highlights import settings


class MessengerBotTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(MessengerBotTestCase, cls).setUpClass()

        helper.class_setup()
        helper.fill_db(TEST_USER_ID)

    def setUp(self):
        self.client = Client()
        helper.set_up(TEST_USER_ID)

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
        self.send_message(TEST_USER_ID, 'Chelsea')
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
                    "text": "Chelsea successfully removed from your subscriptions 👍"
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