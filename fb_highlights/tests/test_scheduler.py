import json

from django.test import TestCase, Client

from fb_bot import scheduler_tasks
from fb_bot.messenger_manager import sender
from fb_bot.model_managers import registration_team_manager, registration_competition_manager, user_manager
from fb_bot.model_managers.latest_highlight_manager import get_highlights, get_recent_highlights_with_incomplete_infos
from fb_highlights.models import LatestHighlight
from fb_highlights.tests.utils import helper
from fb_highlights.tests.utils.assertions import assert_highlight_in, assert_highlight_not_in
from fb_highlights.tests.utils.helper import TEST_USER_ID
from fb_highlights.tests.utils.helper import TIME_40_MINUTES_EARLIER, TIME_NOW, TIME_3_DAYS_EARLIER
from fb_highlights.tests.utils.utils import create_formatted_highlight_response


class SchedulerTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(SchedulerTestCase, cls).setUpClass()

        helper.class_setup()
        helper.fill_db(TEST_USER_ID)

        # Add test registrations
        registration_team_manager.add_team(TEST_USER_ID, "barcelona")
        registration_competition_manager.add_competition(TEST_USER_ID, "premier league")
        registration_competition_manager.add_competition(TEST_USER_ID, "ligue 1")
        registration_competition_manager.add_competition(TEST_USER_ID, "europa league")

    def setUp(self):
        self.client = Client()
        helper.set_up(TEST_USER_ID)

    def send_most_recent_highlights(self):
        scheduler_tasks.send_most_recent_highlights()

    def test_scheduler_send_highlight_message_for_subscribed_team(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_in(
            create_formatted_highlight_response(
                team1='Burnley',
                score1=0,
                team2='Barcelona',
                score2=2,
                competition='Champions League',
                image_url='http://hoofoot/images?burnley-barcelona',
                time=TIME_40_MINUTES_EARLIER
            ), messages)

    def test_scheduler_does_not_send_highlight_message_for_subscribed_team_when_too_recent(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_not_in(
            create_formatted_highlight_response(
                team1='Barcelona',
                score1=1,
                team2='Liverpool',
                score2=1,
                competition='Champions League',
                image_url='http://hoofoot/images?barcelona-liverpool',
                time=TIME_NOW
            ), messages)

    def test_scheduler_sends_highlight_message_for_subscribed_team_when_too_recent_but_priority_is_set(self):
        # Given
        h = LatestHighlight.objects.filter(link='http://hoofoot/barcelona-liverpool')[0]
        h.priority_short = 1
        h.save()

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_in(
            create_formatted_highlight_response(
                team1='Barcelona',
                score1=1,
                team2='Liverpool',
                score2=1,
                competition='Champions League',
                image_url='http://hoofoot/images?barcelona-liverpool',
                time=TIME_NOW
            ), messages)

        # Set back old properties
        h.priority_short = 0
        h.save()

    def test_scheduler_send_highlight_message_for_subscribed_competition(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_in(
            create_formatted_highlight_response(
                team1='Arsenal',
                score1=0,
                team2='Liverpool',
                score2=4,
                competition='Premier League',
                image_url='http://hoofoot/images?arsenal-liverpool',
                time=TIME_40_MINUTES_EARLIER
            ), messages)

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

        assert_highlight_in(
            create_formatted_highlight_response(
                team1='Burnley',
                score1=0,
                team2='Barcelona',
                score2=2,
                competition='Champions League',
                image_url='http://hoofoot/images?burnley-barcelona',
                time=TIME_40_MINUTES_EARLIER,
                score_hidden=True
            ), messages)

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

        assert_highlight_not_in(
            create_formatted_highlight_response(
                team1='Chelsea',
                score1=0,
                team2='Barcelona',
                score2=2,
                competition='Champions League',
                image_url='http://hoofoot/images?chelsea-barcelona2',
                time=TIME_40_MINUTES_EARLIER
            ), messages)

    def test_scheduler_does_not_send_highlight_if_highlight_inverted_home_and_away_teams(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_not_in(
            create_formatted_highlight_response(
                team1='Barcelona',
                score1=2,
                team2='Chelsea',
                score2=0,
                competition='Champions League',
                image_url='http://hoofoot/images?chelsea-barcelona3',
                time=TIME_40_MINUTES_EARLIER
            ), messages)

    def test_scheduler_overrides_picture_and_goals_for_highlights(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_in(
            create_formatted_highlight_response(
                team1='Manchester City',
                score1=0,
                team2='Tottenham',
                score2=0,
                competition='Premier League',
                image_url='http://ourmatch/images?manchester_city-tottenham',
                time=TIME_40_MINUTES_EARLIER
            ), messages)

    def test_scheduler_does_not_send_highlight_with_incomplete_data(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_not_in(
            create_formatted_highlight_response(
                team1='Marseille',
                score1=-1,
                team2='Monaco',
                score2=-1,
                competition='Ligue 1',
                image_url='http://sportyhl/images?marseille-monaco',
                time=TIME_40_MINUTES_EARLIER
            ), messages)

    def test_scheduler_does_not_send_highlight_when_date_too_old(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_not_in(
            create_formatted_highlight_response(
                team1='Swansea',
                score1=0,
                team2='Barcelona',
                score2=3,
                competition='Champions League',
                image_url='http://footyroom/images?swansea-barcelona',
                time=TIME_3_DAYS_EARLIER
            ), messages)

    def test_do_not_send_champions_league(self):
        # Given

        # When
        self.send_most_recent_highlights()

        # Then
        messages = [json.loads(m) for m in sender.CLIENT.messages]

        assert_highlight_not_in(
            create_formatted_highlight_response(
                team1='Swansea',
                score1=2,
                team2='Liverpool',
                score2=0,
                competition='Europa League',
                image_url='http://hoofoot/images?swansea-liverpool',
                time=TIME_40_MINUTES_EARLIER
            ), messages)