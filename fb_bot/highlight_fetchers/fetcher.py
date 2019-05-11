import time

from raven.contrib.django.raven_compat.models import client

from fb_bot.highlight_fetchers import fetcher_footyroom, fetcher_sportyhl, fetcher_highlightsfootball, fetcher_hoofoot, \
    fetcher_our_match, fetcher_youtube
from fb_bot.highlight_fetchers.info import sources
from fb_bot.logger import logger
from fb_bot.model_managers import scrapping_status_manager
from fb_highlights.tests.utils import helper
from highlights import settings

FETCHERS = {
    sources.FOOTYROOM: {
        'fetch': fetcher_footyroom.fetch_highlights,
        'num_pagelet': 3,
        'max_days_ago': 20
    },

    sources.HOOFOOT: {
        'fetch': fetcher_hoofoot.fetch_highlights,
        'num_pagelet': 1,
        'max_days_ago': 20
    },

    sources.HIGHLIGHTS_FOOTBALL: {
        'fetch': fetcher_highlightsfootball.fetch_highlights,
        'num_pagelet': 1,  # Not used
        'max_days_ago': 20
    },

    sources.SPORTYHL: {
        'fetch': fetcher_sportyhl.fetch_highlights,
        'num_pagelet': 3,
        'max_days_ago': 20
    },

    sources.OUR_MATCH: {
        'fetch': fetcher_our_match.fetch_highlights,
        'num_pagelet': 5,
        'max_days_ago': 20
    },

    sources.YOUTUBE: {
        'fetch': fetcher_youtube.fetch_highlights,
        'num_pagelet': 0,  # Not used
        'max_days_ago': 30
    },

    'test_batch_1': {
        'fetch': helper.fetch_test_highlights_batch_1,
        'num_pagelet': 0,
        'max_days_ago': 0
    },

    'test_batch_2': {
        'fetch': helper.fetch_test_highlights_batch_2,
        'num_pagelet': 0,
        'max_days_ago': 0
    }
}


# Define scrapping exception
class ScrappingException(Exception):
    pass


def fetch(site):
    highlights = []
    fetcher = FETCHERS.get(site)

    if not fetcher:
        raise Exception("Fetcher for " + site + " does not exists!")

    num_pagelet = fetcher['num_pagelet']
    max_days_ago = fetcher['max_days_ago']

    try:
        highlights += fetcher['fetch'](num_pagelet=num_pagelet, max_days_ago=max_days_ago)

    except:
        # Say which fetcher failed and the prod status
        client.user_context({
            'prod_status': settings.PROD_STATUS,
            'highlights_fetcher': site
        })
        # Report to sentry problem detected
        client.captureException()

        logger.error("Error while fetching for " + str(site))

    # Update scrapping status in database
    scrapping_status_manager.update_scrapping_status(site, bool(highlights))

    # Tell sentry scrapping problem occurred
    if not highlights:
        raise ScrappingException("Failed to scrape " + site)

    return highlights


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch('footyroom')

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")