import json
from datetime import datetime

from django.test import TestCase, Client

from fb_bot import messenger_manager, scheduler
from fb_bot.model_managers import registration_team_manager, registration_competition_manager
from fb_highlights import tests_helper

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
                "message": {
                    "text": "I am currently sending you the highlights for the following ⚽ teams: \n\n-> No team or competition registered\n\nDo you want to ADD or REMOVE a team?",
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
                "message": {
                    "text": "chelsea was successfully registered 👍"
                }
            },
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
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
                    "text": "I am currently sending you the highlights for the following ⚽ teams: \n\n-> Chelsea\n\nDo you want to ADD or REMOVE a team?"
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
                "message": {
                    "text": "chelsea successfully removed from your subscriptions 👍"
                }
            },
            {
                "recipient": {
                    "id": str(TEST_USER_ID)
                },
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
                    "text": "I am currently sending you the highlights for the following ⚽ teams: \n\n-> No team or competition registered\n\nDo you want to ADD or REMOVE a team?"
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
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League'
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
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League'
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
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=' + str(TEST_USER_ID),
                                        'webview_height_ratio': 'full',
                                        'type': 'web_url',
                                        'messenger_extensions': 'false'
                                    },
                                    'title': 'Chelsea 0 - 2 Barcelona',
                                    'subtitle': 'Champions League'
                                }
                            ]
                        },
                        'type': 'template'
                    }
                }
            }
        ])


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

    def test_scheduler_send_highlight_message_for_subscribed_team(self):
        # Given

        # When
        scheduler.send_most_recent_highlights(footyroom_pagelet=0,
                                              hoofoot_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertIn(
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
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
                                        "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=" + str(TEST_USER_ID)
                                    }
                                }
                            ]
                        }
                    }
                }
            }, messages)

    def test_scheduler_does_not_send_highlight_message_for_subscribed_team_when_too_recent(self):
        # Given

        # When
        scheduler.send_most_recent_highlights(footyroom_pagelet=0,
                                              hoofoot_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertNotIn({
            'recipient': {
                    'id': str(TEST_USER_ID)
            },
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
                                    "url": "http://localhost:8000/highlight?team1=barcelona&score1=1&team2=liverpool&score2=1&date="
                                           + str(datetime.now().date()) + "&user_id=" + str(TEST_USER_ID)
                                }
                            }
                        ]
                    }
                }
            }
        }, messages)

    def test_scheduler_send_highlight_message_for_subscribed_competition(self):
        # Given

        # When
        scheduler.send_most_recent_highlights(footyroom_pagelet=0,
                                              hoofoot_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertIn(
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
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
                                        "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=2018-01-03&user_id=" + str(TEST_USER_ID)
                                    }
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
        scheduler.send_most_recent_highlights(footyroom_pagelet=0,
                                              hoofoot_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertIn(
            {
                'recipient': {
                    'id': str(TEST_USER_ID)
                },
                "message": {
                    "text": "Barcelona ⚽\nL. Messi - 4, 90\nL. Suarez - 43\n\nReal Madrid ⚽\nC. Ronaldo - 10\nS. Ramos - 56"
                }
            },
            messages)