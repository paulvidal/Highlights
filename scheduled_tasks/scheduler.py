# In order to make imports, set python path

import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# Code

import json

from scheduler_helpers import fetcher_highlightsfootball


def fetch_highlightsfootball_highlights(event, context):
    body = []
    highlights = fetcher_highlightsfootball.fetch_highlights()

    for h in highlights:
        body.append({
            'match': h.team1 + ' - ' + h.team2,
            'link': h.link
        })

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


if __name__ == "__main__":
    print(fetch_highlightsfootball_highlights(None, None))