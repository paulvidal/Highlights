from django.test import TestCase, Client

from fb_bot import scheduler_tasks
from fb_bot.model_managers import latest_highlight_manager
from fb_highlights.tests import helper
from fb_highlights.tests.helper import TEST_USER_ID


class FetcherTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(FetcherTestCase, cls).setUpClass()

        helper.class_setup()
        helper.fill_db(TEST_USER_ID)

    def setUp(self):
        self.client = Client()
        helper.set_up(TEST_USER_ID)

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