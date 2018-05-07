import json
from datetime import datetime

from django.test import TestCase, Client

from fb_bot import messenger_manager, scheduler
from fb_bot.messages import *
from fb_bot.model_managers import registration_team_manager, registration_competition_manager, user_manager
from fb_highlights import tests_helper
from fb_highlights.models import LatestHighlight
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
                            "title": "World Cup"
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
                        }
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

    def test_remove_team(self):
        # Given
        self.send_message(TEST_USER_ID, 'subscriptions')
        self.send_message(TEST_USER_ID, 'add')
        self.send_message(TEST_USER_ID, 'chelsea')

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
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League',
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=extended&user_id=' + str(TEST_USER_ID),
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
                    "text": "Tell me for which team should I give you highlight videos? 📺"
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
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League',
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=extended&user_id=' + str(TEST_USER_ID),
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
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League',
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=extended&user_id=' + str(TEST_USER_ID),
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

    def test_change_see_result_setting(self):
        # Given

        # When
        json_response = self.send_message(TEST_USER_ID, 'see result setting')

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
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(
                                            TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(
                                                TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=extended&user_id=' + str(
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

    def setUp(self):
        self.client = Client()
        tests_helper.set_up(TEST_USER_ID)

    def send_most_recent_highlights(self):
        scheduler.send_most_recent_highlights(footyroom_pagelet=0,
                                              hoofoot_pagelet=0,
                                              highlightsfootball_pagelet=0,
                                              sportyhl_pagelet=0)

    def test_scheduler_send_highlight_message_for_subscribed_team(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
                                    "title": "Chelsea 0 - 2 Barcelona",
                                    "subtitle": "Champions League",
                                    "image_url": "http://hoofoot/images?chelsea-barcelona",
                                    "default_action": {
                                        "type": "web_url",
                                        "messenger_extensions": "false",
                                        "webview_height_ratio": "full",
                                        "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=extended&user_id=" + str(TEST_USER_ID),
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
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
                                    "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(datetime.now().date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(datetime.now().date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                        "title": "Short highlight",
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(datetime.now().date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
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
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
                                    "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(datetime.now().date()) + "&type=short&user_id=" + str(TEST_USER_ID)
                                },
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(datetime.now().date()) + "&type=short&user_id=" + str(TEST_USER_ID),
                                        "title": "Short highlight",
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date=" + str(datetime.now().date()) + "&type=extended&user_id=" + str(TEST_USER_ID),
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
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
                                        "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=2018-01-03&type=short&user_id=" + str(TEST_USER_ID)
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=2018-01-03&type=short&user_id=" + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=2018-01-03&type=extended&user_id=" + str(TEST_USER_ID),
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
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

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
                                    'title': 'Chelsea - Barcelona',
                                    'subtitle': 'Champions League',
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=short&user_id=' + str(TEST_USER_ID),
                                            "title": "Short highlight",
                                        },
                                        {
                                            "type": "web_url",
                                            'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&type=extended&user_id=' + str(TEST_USER_ID),
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
