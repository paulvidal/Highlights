import re
import time

import dateparser
import requests

from fb_bot.highlight_fetchers.info import sources
from fb_bot.highlight_fetchers.utils.Highlight import Highlight
from highlights import settings

PART = "snippet"
CHANNEL_ID = "UCQsH5XtIc9hONE1BQjucM0g"
ORDER = "date"
MAX_RESULT = "50"
API_KEY = settings.get_env_var('YOUTUBE_KEY')
URL = "https://www.googleapis.com/youtube/v3/search?part={}&channelId={}&order={}&maxResults={}&key={}".format(
    PART,
    CHANNEL_ID,
    ORDER,
    MAX_RESULT,
    API_KEY
)
YOUTUBE_LINK = "https://www.youtube.com/watch?v={}"


class YoutubeHighlight(Highlight):

    def __init__(self, link, match_name, img_link, view_count, category, time_since_added, type='normal'):
        super().__init__(link, match_name, img_link, view_count, category, time_since_added, goal_data=[], type=type)

    def get_match_info(self, match):
        team1, team2 = self._parse_team_names(match)
        score1, score2 = self._parse_scores(match)

        return team1, score1, team2, score2

    @staticmethod
    def _parse_team_names(match):
        regex = "(.*?)\("
        search_result = re.compile(regex, 0).search(match).groups()[0]
        teams = [team.strip() for team in search_result.split(' - ')]
        return teams[0], teams[1]

    @staticmethod
    def _parse_scores(match):
        regex = "\((.*?)\)"
        search_result = re.compile(regex, 0).search(match).groups()[0]
        scores = [int(score.strip()) for score in search_result.split('-')]
        return scores[0], scores[1]

    def get_source(self):
        return sources.YOUTUBE


def fetch_highlights(num_pagelet, max_days_ago):
    highlights = []

    response = requests.get(URL).json()
    items = response['items']

    for video in items:
        match_name = video['snippet']['title']

        if '- Résumé -' in match_name:
            id = video['id']['videoId']
            img_url = video['snippet']['thumbnails']['high']['url'] if video['snippet']['thumbnails'].get('high') else video['snippet']['thumbnails']['default']['url']
            time_since_added = dateparser.parse(video['snippet']['publishedAt']).replace(tzinfo=None)

            highlights.append(YoutubeHighlight(
                form_link(id),
                match_name,
                img_url,
                0,
                'ligue 1',
                time_since_added,
            ))

    return highlights


def form_link(id):
    return YOUTUBE_LINK.format(id)


if __name__ == "__main__":
    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights(num_pagelet=1, max_days_ago=40)

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")