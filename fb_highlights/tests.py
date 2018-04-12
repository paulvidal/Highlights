import json

import dateparser
from django.test import TestCase, Client

from fb_bot.highlight_fetchers.fetcher_hoofoot import HoofootHighlight
from fb_bot.logger import logger
from fb_bot.model_managers import football_team_manager, latest_highlight_manager, context_manager

SENDER_ID = 1119096411506599


class MessengerBotTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MessengerBotTestCase, cls).setUpClass()

        logger.disable()

        # Set up test database
        football_team_manager.add_football_team("chelsea")
        football_team_manager.add_football_team("barcelona")

        latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot?chelsea-barcelona',
                                                                'Chelsea 0 - 2 Barcelona',
                                                                'http://hoofoot/images?chelsea-barcelona',
                                                                0,
                                                                'Champions League',
                                                                dateparser.parse('2018-01-01')))

    def setUp(self):
        self.client = Client()
        context_manager.set_default_context(SENDER_ID)

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

    # TESTS

    def test_my_teams(self):
        # Given

        # When
        json_response = self.send_message(SENDER_ID, 'teams')

        # Then
        self.assertEqual(json_response, [
            {
                "message": {
                    "text": "I am currently sending you the highlights for the following ⚽ teams: \n\n-> No team registered\n\nDo you want to ADD or REMOVE a team?",
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

    def test_add_teams(self):
        # Given
        self.send_message(SENDER_ID, 'teams')

        # When
        json_response = self.send_message(SENDER_ID, 'add')

        # Then
        self.assertEqual(json_response, [
            {
                "recipient": {
                    "id": "1119096411506599"
                },
                "message": {
                    "text": "Tell me the name of the team you want to add 🔥"
                }
            }
        ])

    def test_adding_chelsea(self):
        # Given
        self.send_message(SENDER_ID, 'teams')
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
                    "text": "chelsea was successfully added to your teams 👍"
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
        self.send_message(SENDER_ID, 'teams')
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
                    "text": "Which team do you want to remove?"
                }
            }
        ])

    def test_removing_chelsea(self):
        # Given
        self.send_message(SENDER_ID, 'teams')
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
                    "text": "chelsea successfully removed from your teams 👍"
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
                    "text": "I am currently sending you the highlights for the following ⚽ teams: \n\n-> No team registered\n\nDo you want to ADD or REMOVE a team?"
                }
            }
        ])

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
                                    'subtitle': '01 January 2018 - Champions League'
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
                                    'subtitle': '01 January 2018 - Champions League'
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
                                    'subtitle': '01 January 2018 - Champions League'
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