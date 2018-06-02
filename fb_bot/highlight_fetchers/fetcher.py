import time
from raven.contrib.django.raven_compat.models import client

from fb_bot.highlight_fetchers import fetcher_footyroom, fetcher_sportyhl, fetcher_highlightsfootball, fetcher_hoofoot, fetcher_our_match
from fb_bot.highlight_fetchers.info import sources
from highlights import settings

FETCHERS = [
    {
        'name': sources.FOOTYROOM,
        'fetch': fetcher_footyroom.fetch_highlights,
        'num_pagelet': 3,
        'max_days_ago': 20
    },
    {
        'name': sources.HOOFOOT,
        'fetch': fetcher_hoofoot.fetch_highlights,
        'num_pagelet': 3,
        'max_days_ago': 20
    },
    {
        'name': sources.HIGHLIGHTS_FOOTBALL,
        'fetch': fetcher_highlightsfootball.fetch_highlights,
        'num_pagelet': 3,
        'max_days_ago': 20
    },
    {
        'name': sources.SPORTYHL,
        'fetch': fetcher_sportyhl.fetch_highlights,
        'num_pagelet': 3,
        'max_days_ago': 20
    },
    {
        'name': sources.OUR_MATCH,
        'fetch': fetcher_our_match.fetch_highlights,
        'num_pagelet': 5,
        'max_days_ago': 20
    }
]


# General fetch method which is fail SAFE (one fetcher failing won't affect the others)
def fetch_all_highlights():

    highlights = []

    for fetcher in FETCHERS:
        num_pagelet = fetcher['num_pagelet']
        max_days_ago = fetcher['max_days_ago']

        try:
            highlights += fetcher['fetch'](num_pagelet=num_pagelet, max_days_ago=max_days_ago)
        except:
            # Say which fetcher failed and the prod status
            client.user_context({
                'prod_status': settings.PROD_STATUS,
                'highlights_fetcher': fetcher['name']
            })
            # Report to sentry problem detected
            client.captureException()

    return highlights


# Check status of fetching
def get_fetching_status():
    scrapping_problems = []

    for fetcher in FETCHERS:
        num_pagelet = 1
        max_days_ago = 1000

        highlights = fetcher['fetch'](num_pagelet=num_pagelet, max_days_ago=max_days_ago)

        if not highlights:
            scrapping_problems.append(fetcher['name'])

    return scrapping_problems


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_all_highlights()

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")