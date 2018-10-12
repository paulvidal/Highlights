from datetime import datetime, timedelta

from fb_bot.messenger_manager import sender
from fb_bot.highlight_fetchers.fetcher_footyroom import FootyroomVideoHighlight, FootyroomHighlight
from fb_bot.highlight_fetchers.fetcher_hoofoot import HoofootHighlight
from fb_bot.highlight_fetchers.fetcher_our_match import OurMatchHighlight
from fb_bot.highlight_fetchers.fetcher_sportyhl import SportyHLHighlight
from fb_bot.logger import logger
from fb_bot.model_managers import football_team_manager, football_competition_manager, latest_highlight_manager, \
    context_manager
from fb_highlights.models import User


TEST_USER_ID = 1119096411506599

TIME_NOW = datetime.now()
TIME_40_MINUTES_EARLIER = datetime.now() - timedelta(minutes=40)
TIME_1_DAY_EARLIER = datetime.now() - timedelta(hours=24)
TIME_3_DAYS_EARLIER = datetime.now() - timedelta(hours=72)


def class_setup():
    logger.disable()
    sender.CLIENT.disable()


def set_up(test_user_id):
    context_manager.set_default_context(test_user_id)
    sender.CLIENT.messages = []


# Set up test database
def fill_db(test_user_id):

    # Create a test user
    User.objects.update_or_create(facebook_id=test_user_id,
                                  first_name="first",
                                  last_name="last",
                                  locale="en_GB",
                                  timezone=0)

    # Add teams
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


    # Add competitions
    football_competition_manager.add_football_competition('ligue 1')
    football_competition_manager.add_football_competition('champions league')
    football_competition_manager.add_football_competition('europa league')
    football_competition_manager.add_football_competition('premier league')
    football_competition_manager.add_football_competition('la liga')

    # Add highlights
    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona',
                                                            'Chelsea 0 - 2 Barcelona',
                                                            'http://hoofoot/img?chelsea-barcelona',
                                                            0,
                                                            'Champions League',
                                                            TIME_40_MINUTES_EARLIER), sent=True)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona2',
                                                            'Chelsea 0 - 2 Barcelona',
                                                            'http://hoofoot/img?chelsea-barcelona2',
                                                            0,
                                                            'Champions League',
                                                            TIME_40_MINUTES_EARLIER), sent=False)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona3',
                                                            'Barcelona 2 - 0 Chelsea',
                                                            'http://hoofoot/img?chelsea-barcelona3',
                                                            0,
                                                            'Champions League',
                                                            TIME_40_MINUTES_EARLIER), sent=False)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/burnley-barcelona',
                                                            'Burnley 0 - 2 Barcelona',
                                                            'http://hoofoot/img?burnley-barcelona',
                                                            0,
                                                            'Champions League',
                                                            TIME_40_MINUTES_EARLIER), sent=False)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-real_madrid',
                                                            'Arsenal 1 - 0 Real Madrid',
                                                            'http://hoofoot/img?chelsea-real_madrid',
                                                            0,
                                                            'Champions League',
                                                            TIME_40_MINUTES_EARLIER))

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/arsenal-liverpool',
                                                            'Arsenal 0 - 4 Liverpool',
                                                            'http://hoofoot/img?arsenal-liverpool',
                                                            0,
                                                            'Premier League',
                                                            TIME_40_MINUTES_EARLIER))

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/barcelona-liverpool',
                                                            'Barcelona 1 - 1 Liverpool',
                                                            'http://hoofoot/img?barcelona-liverpool',
                                                            0,
                                                            'Champions League',
                                                            TIME_NOW))

    latest_highlight_manager.add_highlight(FootyroomVideoHighlight('http://hoofoot/barcelona-real_madrid',
                                                                   'Barcelona 3 - 2 Real Madrid',
                                                                   'http://footyroom/img?barcelona-real_madrid',
                                                                   0,
                                                                   'La Liga',
                                                                   TIME_40_MINUTES_EARLIER,
                                                                   [
                                                                       {'team': 1, 'player': 'Lionel Messi', 'elapsed': 4, 'goal_type': 'penalty'},
                                                                       {'team': 2, 'player': 'Cristiano Ronaldo', 'elapsed': 10, 'goal_type': 'goal'},
                                                                       {'team': 1, 'player': 'Luis Suarez', 'elapsed': 43, 'goal_type': 'goal'},
                                                                       {'team': 2, 'player': 'Gerard Pique', 'elapsed': 56, 'goal_type': 'own goal'},
                                                                       {'team': 1, 'player': 'Lionel Messi', 'elapsed': 90, 'goal_type': 'goal'}
                                                                   ]))

    latest_highlight_manager.add_highlight(FootyroomVideoHighlight('http://hoofoot/barcelona-arsenal',
                                                                   'Barcelona 0 - 1 Arsenal',
                                                                   'http://footyroom/img?barcelona-arsenal',
                                                                   0,
                                                                   'Champions League',
                                                                   TIME_40_MINUTES_EARLIER,
                                                                   [
                                                                       {'team': 2, 'player': 'Olivier Giroud', 'elapsed': 15, 'goal_type': 'goal'}
                                                                   ]))

    latest_highlight_manager.add_highlight(FootyroomHighlight('http://footyroom/manchester_city-tottenham2',
                                                              'Manchester City 0 - 0 Tottenham',
                                                              'http://footyroom/img?manchester_city-tottenham',
                                                              0,
                                                              'Premier League',
                                                              TIME_1_DAY_EARLIER))

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/manchester_city-tottenham',
                                                            'Manchester City 0 - 0 Tottenham',
                                                            'http://hoofoot/img?manchester_city-tottenham',
                                                            0,
                                                            'Premier League',
                                                            TIME_40_MINUTES_EARLIER))

    latest_highlight_manager.add_highlight(OurMatchHighlight('http://ourmatch/manchester_city-tottenham',
                                                             'Manchester City vs Tottenham',
                                                             'http://ourmatch/img?manchester_city-tottenham',
                                                             0,
                                                             'Premier League',
                                                             TIME_40_MINUTES_EARLIER, [], 'normal').set_score(0, 0))

    latest_highlight_manager.add_highlight(FootyroomHighlight('http://footyroom/manchester_city-tottenham',
                                                              'Manchester City 0 - 0 Tottenham',
                                                              'http://footyroom/img?manchester_city-tottenham',
                                                              0,
                                                              'Premier League',
                                                              TIME_40_MINUTES_EARLIER))

    latest_highlight_manager.add_highlight(SportyHLHighlight('http://sportyhl/marseille-monaco',
                                                             'Marseille vs Monaco',
                                                             'http://sportyhl/img?marseille-monaco',
                                                             0,
                                                             'Ligue 1',
                                                             TIME_40_MINUTES_EARLIER, 'normal'))

    latest_highlight_manager.add_highlight(SportyHLHighlight('http://sportyhl/marseille-monaco-2',
                                                             'Marseille vs Monaco',
                                                             'http://sportyhl/img?marseille-monaco',
                                                             0,
                                                             'Ligue 1',
                                                             TIME_3_DAYS_EARLIER, 'normal'), sent=True)

    latest_highlight_manager.add_highlight(FootyroomHighlight('http://footyroom/swansea-barcelona',
                                                             'Swansea 0 - 3 Barcelona',
                                                             'http://footyroom/img?swansea-barcelona',
                                                             0,
                                                             'Champions League',
                                                              TIME_3_DAYS_EARLIER))

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/swansea-arsenal',
                                                            'Swansea 4 - 0 Arsenal',
                                                            'http://hoofoot/img?swansea-arsenal',
                                                            0,
                                                            'Premier League',
                                                            TIME_40_MINUTES_EARLIER), sent=True)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/swansea-liverpool',
                                                            'Swansea 2 - 0 Liverpool',
                                                            'http://hoofoot/img?swansea-liverpool',
                                                            0,
                                                            'Europa League',
                                                            TIME_40_MINUTES_EARLIER))


def fetch_test_highlights(num_pagelet, max_days_ago):
    highlight = [
        FootyroomHighlight(
            'http://footyroom/chelsea-barcelona4',
            'Barcelona 2 - 0 Chelsea',
            'http://footyroom/img?chelsea-barcelona4',
            0,
            'Champions League',
            str(TIME_40_MINUTES_EARLIER)
        ),
        HoofootHighlight(
            'http://hoofoot/arsenal-liverpool2',
            'Liverpool 4 - 0 Arsenal',
            'http://hoofoot/img?arsenal-liverpool',
            0,
            'Premier League',
            str(TIME_40_MINUTES_EARLIER)
        ),
        HoofootHighlight(
            'http://hoofoot/swansea-arsenal2',
            'Arsenal 0 - 4 Swansea',
            'http://hoofoot/img?swansea-arsenal',
            0,
            'Premier League',
            str(TIME_40_MINUTES_EARLIER)
        ),
    ]

    return highlight