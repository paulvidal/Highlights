from fb_bot.logger import logger
from fb_bot.messenger_manager import sender
from fb_bot.model_managers import football_team_manager, football_competition_manager, latest_highlight_manager, \
    context_manager
from fb_highlights.models import User, HighlightImage
from fb_highlights.tests.utils.test_highlights import TEST_HIGHLIGHTS, SENT_HIGHLIGHTS, INCREMENT_CLICK_COUNT, \
    TEST_HIGHLIGHTS_2, TEST_IMAGE, TEST_UPLOADED_IMAGE

TEST_USER_ID = 1119096411506599


def class_setup():
    logger.disable()
    sender.CLIENT.disable()


def set_up(test_user_id):
    context_manager.set_default_context(test_user_id)
    sender.CLIENT.messages = []


# Simulate fetched highlights
def fetch_test_highlights_batch_1(num_pagelet, max_days_ago):
    return TEST_HIGHLIGHTS


def fetch_test_highlights_batch_2(num_pagelet, max_days_ago):
    return TEST_HIGHLIGHTS_2


# Initialise test database
def init_db(test_user_id):

    # Create a test user
    User.objects.update_or_create(facebook_id=test_user_id,
                                  first_name="first",
                                  last_name="last",
                                  locale="en_GB",
                                  timezone=0)

    # Create teams
    football_team_manager.add_football_team("chelsea")
    football_team_manager.add_football_team("barcelona")
    football_team_manager.add_football_team("real madrid")
    football_team_manager.add_football_team("arsenal")
    football_team_manager.add_football_team("liverpool")
    football_team_manager.add_football_team("burnley")
    football_team_manager.add_football_team("swansea")
    football_team_manager.add_football_team("tottenham")
    football_team_manager.add_football_team("manchester city")
    football_team_manager.add_football_team("marseille")
    football_team_manager.add_football_team("monaco")
    football_team_manager.add_football_team("france")
    football_team_manager.add_football_team("england")
    football_team_manager.add_football_team("belgium")

    # Create competitions
    football_competition_manager.add_football_competition('ligue 1')
    football_competition_manager.add_football_competition('champions league')
    football_competition_manager.add_football_competition('europa league')
    football_competition_manager.add_football_competition('premier league')
    football_competition_manager.add_football_competition('la liga')
    football_competition_manager.add_football_competition('nations league')

    # Create image mappings
    for match_id in [17, 18, 19, 20]:
        HighlightImage.objects.update_or_create(match_id=match_id,
                                                img_link=TEST_IMAGE,
                                                img_uploaded_link=TEST_UPLOADED_IMAGE,
                                                source='ourmatch')


# Modify elements in database
def set_up_db():
    # Set highlights send
    for link in SENT_HIGHLIGHTS:
        h = latest_highlight_manager.get_highlight(link)
        latest_highlight_manager.set_sent(h)

    # Set highlights click counts
    for link, count in INCREMENT_CLICK_COUNT:
        h = latest_highlight_manager.get_highlight(link)
        for _ in range(count):
            latest_highlight_manager.increment_click_count(h)