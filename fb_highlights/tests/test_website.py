from django.test import TestCase, Client

from fb_highlights.tests.utils import helper
from fb_highlights.tests.utils.helper import TEST_USER_ID

from fb_highlights.tests.utils.helper import TIME_40_MINUTES_EARLIER


class WebsiteTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(WebsiteTestCase, cls).setUpClass()

        helper.class_setup()
        helper.fill_db(TEST_USER_ID)

    def setUp(self):
        self.client = Client()
        helper.set_up(TEST_USER_ID)

    def get_highlights(self, count=10, search=None):
        url = '/highlights?count={}'.format(count)

        if search:
            url += '&search={}'.format(search)

        response = self.client.get(url)

        return response.json()

    # WEBSITE TESTS

    def test_highlights_are_sent_in_the_right_order(self):
        # Given

        # When
        json_response = self.get_highlights(count=2)

        # Then
        self.assertEqual(json_response, {
            'highlights': [
                {
                    'view_count': 2,
                    'category': 'premier league',
                    'team1': 'swansea',
                    'score1': 4,
                    'team2': 'arsenal',
                    'score2': 0,
                    'link': 'http://localhost:8000/highlight?team1=swansea&score1=4&team2=arsenal&score2=0&date={}&type=short'.format(str(TIME_40_MINUTES_EARLIER.date())),
                    'link_extended': 'http://localhost:8000/highlight?team1=swansea&score1=4&team2=arsenal&score2=0&date={}&type=extended'.format(str(TIME_40_MINUTES_EARLIER.date())),
                    'img_link': 'http://hoofoot/img?swansea-arsenal',
                    'match_time': TIME_40_MINUTES_EARLIER.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S"),
                },
                {
                    'view_count': 1,
                    'category': 'europa league',
                    'team1': 'swansea',
                    'score1': 2,
                    'team2': 'liverpool',
                    'score2': 0,
                    'link': 'http://localhost:8000/highlight?team1=swansea&score1=2&team2=liverpool&score2=0&date={}&type=short'.format(str(TIME_40_MINUTES_EARLIER.date())),
                    'link_extended': 'http://localhost:8000/highlight?team1=swansea&score1=2&team2=liverpool&score2=0&date={}&type=extended'.format(str(TIME_40_MINUTES_EARLIER.date())),
                    'img_link': 'http://hoofoot/img?swansea-liverpool',
                    'match_time': TIME_40_MINUTES_EARLIER.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S"),
                }
            ],
            'suggestions': []
        })

    def test_search(self):
        # Given

        # When
        json_response = self.get_highlights(count=1, search='barcelona')

        # Then
        self.assertEqual(json_response, {
            'highlights': [
                {
                    'view_count': 0,
                    'category': 'champions league',
                    'team1': 'barcelona',
                    'score1': 0,
                    'team2': 'arsenal',
                    'score2': 1,
                    'link': 'http://localhost:8000/highlight?team1=barcelona&score1=0&team2=arsenal&score2=1&date={}&type=short'.format(str(TIME_40_MINUTES_EARLIER.date())),
                    'link_extended': 'http://localhost:8000/highlight?team1=barcelona&score1=0&team2=arsenal&score2=1&date={}&type=extended'.format(str(TIME_40_MINUTES_EARLIER.date())),
                    'img_link': 'http://footyroom/img?barcelona-arsenal',
                    'match_time': TIME_40_MINUTES_EARLIER.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S"),
                }
            ],
            'suggestions': []
        })

    def test_suggestion(self):
        # Given

        # When
        json_response = self.get_highlights(count=2, search='arsena')

        # Then
        self.assertEqual(json_response, {
            'highlights': [],
            'suggestions': [
                'arsenal'
            ]
        })