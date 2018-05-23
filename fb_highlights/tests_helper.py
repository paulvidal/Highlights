from datetime import datetime

import dateparser

from fb_bot import messenger_manager
from fb_bot.highlight_fetchers.fetcher_footyroom import FootyroomVideoHighlight, FootyroomHighlight
from fb_bot.highlight_fetchers.fetcher_hoofoot import HoofootHighlight
from fb_bot.highlight_fetchers.fetcher_our_match import OurMatchHighlight
from fb_bot.highlight_fetchers.fetcher_sportyhl import SportyHLHighlight
from fb_bot.logger import logger
from fb_bot.model_managers import football_team_manager, football_competition_manager, latest_highlight_manager, \
    context_manager
from fb_highlights.models import User


def class_setup():
    logger.disable()
    messenger_manager.CLIENT.disable()


def set_up(test_user_id):
    context_manager.set_default_context(test_user_id)
    messenger_manager.CLIENT.messages = []


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
    football_team_manager.add_football_team("tottenham")
    football_team_manager.add_football_team("manchester city")
    football_team_manager.add_football_team("marseille")
    football_team_manager.add_football_team("monaco")


    # Add competitions
    football_competition_manager.add_football_competition('ligue 1')
    football_competition_manager.add_football_competition('champions league')
    football_competition_manager.add_football_competition('premier league')
    football_competition_manager.add_football_competition('la liga')

    # Add highlights
    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona',
                                                            'Chelsea 0 - 2 Barcelona',
                                                            'http://hoofoot/images?chelsea-barcelona',
                                                            0,
                                                            'Champions League',
                                                            dateparser.parse('2018-01-01')), sent=True)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona2',
                                                            'Chelsea 0 - 2 Barcelona',
                                                            'http://hoofoot/images?chelsea-barcelona2',
                                                            0,
                                                            'Champions League',
                                                            dateparser.parse('2018-01-01')), sent=False)

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/chelsea-barcelona3',
                                                            'Chelsea 0 - 2 Barcelona',
                                                            'http://hoofoot/images?chelsea-barcelona3',
                                                            0,
                                                            'Champions League',
                                                            dateparser.parse('2018-01-05')), sent=False)

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

    latest_highlight_manager.add_highlight(FootyroomVideoHighlight('http://hoofoot/barcelona-real_madrid',
                                                                   'Barcelona 3 - 2 Real Madrid',
                                                                   'http://footyroom/images?barcelona-real_madrid',
                                                                   0,
                                                                   'La Liga',
                                                                   dateparser.parse('2018-01-05'),
                                                                   [
                                                                       {'team': 1, 'player': 'Lionel Messi', 'elapsed': 4, 'goal_type': 'penalty'},
                                                                       {'team': 2, 'player': 'Cristiano Ronaldo', 'elapsed': 10, 'goal_type': 'goal'},
                                                                       {'team': 1, 'player': 'Luis Suarez', 'elapsed': 43, 'goal_type': 'goal'},
                                                                       {'team': 2, 'player': 'Gerard Pique', 'elapsed': 56, 'goal_type': 'own goal'},
                                                                       {'team': 1, 'player': 'Lionel Messi', 'elapsed': 90, 'goal_type': 'goal'}
                                                                   ]))

    latest_highlight_manager.add_highlight(FootyroomVideoHighlight('http://hoofoot/barcelona-arsenal',
                                                                   'Barcelona 0 - 1 Arsenal',
                                                                   'http://footyroom/images?barcelona-arsenal',
                                                                   0,
                                                                   'Champions League',
                                                                   dateparser.parse('2018-01-06'),
                                                                   [
                                                                       {'team': 2, 'player': 'Olivier Giroud', 'elapsed': 15, 'goal_type': 'goal'}
                                                                   ]))

    latest_highlight_manager.add_highlight(HoofootHighlight('http://hoofoot/manchester_city-tottenham',
                                                            'Manchester City 0 - 0 Tottenham',
                                                            'http://hoofoot/images?manchester_city-tottenham',
                                                            0,
                                                            'Premier League',
                                                            dateparser.parse('2018-01-08')))

    latest_highlight_manager.add_highlight(OurMatchHighlight('http://ourmatch/manchester_city-tottenham',
                                                             'Manchester City vs Tottenham',
                                                             'http://ourmatch/images?manchester_city-tottenham',
                                                             0,
                                                             'Premier League',
                                                             dateparser.parse('2018-01-08'), [], 'normal').set_score(0, 0))

    latest_highlight_manager.add_highlight(FootyroomHighlight('http://footyroom/manchester_city-tottenham',
                                                              'Manchester City 0 - 0 Tottenham',
                                                              'http://footyroom/images?manchester_city-tottenham',
                                                              0,
                                                              'Premier League',
                                                              dateparser.parse('2018-01-08')))

    latest_highlight_manager.add_highlight(SportyHLHighlight('http://sportyhl/marseille-monaco',
                                                             'Marseille vs Monaco',
                                                             'http://sportyhl/images?marseille-monaco',
                                                             0,
                                                             'Ligue 1',
                                                             dateparser.parse('2018-01-09'), 'normal'))

    latest_highlight_manager.add_highlight(SportyHLHighlight('http://sportyhl/marseille-monaco-2',
                                                             'Marseille vs Monaco',
                                                             'http://sportyhl/images?marseille-monaco',
                                                             0,
                                                             'Ligue 1',
                                                             dateparser.parse('2018-01-09'), 'normal'), sent=True)