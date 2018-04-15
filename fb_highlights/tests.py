import json
from datetime import datetime, timedelta

import dateparser
from django.test import TestCase, Client

from fb_bot import messenger_manager, scheduler
from fb_bot.highlight_fetchers.fetcher_hoofoot import HoofootHighlight
from fb_bot.logger import logger
from fb_bot.model_managers import football_team_manager, latest_highlight_manager, context_manager, football_competition_manager, \
    registration_team_manager, registration_competition_manager
from fb_highlights.models import User

SENDER_ID = 1119096411506599


class MessengerBotTestCase(TestCase):

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(MessengerBotTestCase, cls).setUpClass()

        logger.disable()
        messenger_manager.CLIENT.disable()

        # Set up test database
        User.objects.update_or_create(facebook_id=0,
                                      first_name="first",
                                      last_name="last",
                                      image_url="http://images/url.png",
                                      locale="en_GB",
                                      timezone=0,
                                      gender="male")

        football_team_manager.add_football_team("chelsea")
        football_team_manager.add_football_team("barcelona")
        football_team_manager.add_football_team("real madrid")
        football_team_manager.add_football_team("arsenal")
        football_team_manager.add_football_team("liverpool")

        football_competition_manager.add_football_competition('champions league')
        football_competition_manager.add_football_competition('premier league')

        latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona',
                                                                'Chelsea 0 - 2 Barcelona',
                                                                'http://hoofoot/images?chelsea-barcelona',
                                                                0,
                                                                'Champions League',
                                                                dateparser.parse('2018-01-01')))

        latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-real_madrid',
                                                                'Arsenal 1 - 0 Real Madrid',
                                                                'http://hoofoot/images?chelsea-real_madrid',
                                                                0,
                                                                'Champions League',
                                                                dateparser.parse('2018-01-02')))

        latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/arsenal-liverpool',
                                                                'Arsenal 0 - 4 Liverpool',
                                                                'http://hoofoot/images?arsenal-liverpool',
                                                                0,
                                                                'Premier League',
                                                                dateparser.parse('2018-01-03')))

        latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/barcelona-liverpool',
                                                                'Barcelona 1 - 1 Liverpool',
                                                                'http://hoofoot/images?barcelona-liverpool',
                                                                0,
                                                                'Champions League',
                                                                datetime.now()))

        registration_team_manager.add_team(0, "barcelona")
        registration_competition_manager.add_competition(0, "premier league")

    def setUp(self):
        self.client = Client()
        context_manager.set_default_context(SENDER_ID)
        messenger_manager.CLIENT.messages = []

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
        json_response = self.send_message(SENDER_ID, 'subscriptions')

        # Then
        self.assertEqual(json_response, [
            {
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
                },
                "recipient": {
                    "id": "1119096411506599"
                }
            }
        ])

    def test_add_team_subscription(self):
        # Given
        self.send_message(SENDER_ID, 'subscriptions')

        # When
        json_response = self.send_message(SENDER_ID, 'add')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": "1119096411506599"
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
                            "title": "Barcelona"
                        },
                        {
                            "content_type": "text",
                            "payload": "NO_PAYLOAD",
                            "title": "Champions League"
                        }
                    ],
                }
            }
        ])

    def test_adding_chelsea(self):
        # Given
        self.send_message(SENDER_ID, 'subscriptions')
        self.send_message(SENDER_ID, 'add')

        # When
        json_response = self.send_message(SENDER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": "1119096411506599"
                },
                "message": {
                    "text": "chelsea was successfully registered 👍"
                }
            },
            {
                "recipient": {
                    "id": "1119096411506599"
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
        self.send_message(SENDER_ID, 'subscriptions')
        self.send_message(SENDER_ID, 'add')
        self.send_message(SENDER_ID, 'chelsea')

        # When
        json_response = self.send_message(SENDER_ID, 'remove')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": "1119096411506599"
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
        self.send_message(SENDER_ID, 'subscriptions')
        self.send_message(SENDER_ID, 'add')
        self.send_message(SENDER_ID, 'chelsea')
        self.send_message(SENDER_ID, 'remove')

        # When
        json_response = self.send_message(SENDER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": "1119096411506599"
                },
                "message": {
                    "text": "chelsea successfully removed from your subscriptions 👍"
                }
            },
            {
                "recipient": {
                    "id": "1119096411506599"
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
        json_response = self.send_message(SENDER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=1119096411506599',
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
                },
                'recipient': {
                    'id': '1119096411506599'
                }
            }
        ])

    def test_search(self):
        # Given

        # When
        json_response = self.send_message(SENDER_ID, 'search')

        # Then
        self.assertEqual(json_response, [
            {
                "message": {
                    "text": "Tell me for which team should I give you highlight videos? 📺"
                },
                "recipient": {
                    "id": "1119096411506599"
                }
            }
        ])

    def test_search_chelsea(self):
        # Given
        self.send_message(SENDER_ID, 'search')

        # When
        json_response = self.send_message(SENDER_ID, 'chelsea')

        # Then
        self.assertEqual(json_response, [
            {
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=1119096411506599',
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
                },
                'recipient': {
                    'id': '1119096411506599'
                }
            }
        ])

    def test_search_chelsea_with_typo(self):
        # Given
        self.send_message(SENDER_ID, 'search')

        # When
        json_response = self.send_message(SENDER_ID, 'chelseo')

        # Then
        self.assertEqual(json_response, [
            {
                'message': {
                    'attachment': {
                        'payload': {
                            'template_type': 'generic',
                            'elements': [
                                {
                                    'image_url': 'http://hoofoot/images?chelsea-barcelona',
                                    'default_action': {
                                        'url': 'http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=1119096411506599',
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
                },
                'recipient': {
                    'id': '1119096411506599'
                }
            }
        ])

    # SCHEDULER TESTS

    def test_scheduler_send_highlight_message_for_subscribed_team(self):
        # Given

        # When
        scheduler.send_most_recent_highlights(footyroom_pagelet=0,
                                              hoofoot_pagelet=0,
                                              footyroom_videos_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertIn(
            {
                "recipient": {
                    "id": 0
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
                                        "url": "http://localhost:8000/highlight?team1=chelsea&score1=0&team2=barcelona&score2=2&date=2018-01-01&user_id=0"
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
                                              hoofoot_pagelet=0,
                                              footyroom_videos_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertNotIn({
            "recipient": {
                "id": 0
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
                                           + str(datetime.now().date()) + "&user_id=0"
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
                                              hoofoot_pagelet=0,
                                              footyroom_videos_pagelet=0)

        # Then
        messages = [json.loads(m) for m in messenger_manager.CLIENT.messages]

        self.assertIn(
            {
                "recipient": {
                    "id": 0
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
                                        "url": "http://localhost:8000/highlight?team1=arsenal&score1=0&team2=liverpool&score2=4&date=2018-01-03&user_id=0"
                                    }
                                }
                            ]
                        }
                    }
                }
            },
            messages)