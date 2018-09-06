import time
from datetime import datetime

import dateparser
import re
import requests
from bs4 import BeautifulSoup

from fb_bot.highlight_fetchers import fetcher_footyroom
from fb_bot.highlight_fetchers.info import providers, sources
from fb_bot.highlight_fetchers.utils.Highlight import Highlight
from fb_bot.highlight_fetchers.utils.link_formatter import format_dailymotion_link, format_streamable_link, format_link

ROOT_URL = 'https://highlightsfootball.com'


class HighlightsFootballHighlight(Highlight):

    def __init__(self, link, match_name, img_link, view_count, category, time_since_added):
        super().__init__(link, match_name, img_link, view_count, category, time_since_added, goal_data=[], type='normal')

    def get_match_info(self, match):
        match = match.replace('Highlights', '').strip()

        match_split = match.split()
        middle_index = match_split.index('vs')

        def join(l):
            return " ".join(l)

        team1 = join(match_split[:middle_index])
        score1 = -1
        team2 = join(match_split[middle_index + 1:])
        score2 = -1

        return team1, score1, team2, score2

    def get_source(self):
        return sources.HIGHLIGHTS_FOOTBALL


def fetch_highlights(num_pagelet=4, max_days_ago=7):
    """
    Fetch all the possible highlights available on highlightsfootball given a number of pagelet to look at
    (15 highlights per pagelet)

    :param num_pagelet: number of pagelet to consider
    :param max_days_ago: max age of a highlight (after this age, we don't consider the highlight)
    :return: the latests highlights available on highlightsfootball
    """

    highlights = []

    for pagelet_num in range(num_pagelet):
        highlights += _fetch_pagelet_highlights(pagelet_num, max_days_ago)

    return highlights


def _fetch_pagelet_highlights(pagelet_num, max_days_ago):
    highlights = []

    page = requests.get(ROOT_URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Extract videos
    for vid in soup.find_all(class_='td_module_flex_1'):

        # Extract match name
        match_name = str(vid.find(class_='td-image-wrap').get('title'))

        if not 'vs' in match_name:
            # Check that the highlight is for a match
            continue

        # Extract view count - NOT AVAILABLE for this website
        view_count = 0

        # Extract category
        info = vid.find(class_='td-post-category')

        if not info:
            continue

        category = str(info.get_text())

        # Extract time since video added
        date = vid.find(class_='td-module-date')

        if not date:
            continue

        now = datetime.now()

        time_since_added = str(date.get_text())
        time_since_added_date = dateparser.parse(time_since_added).replace(hour=now.hour, minute=now.minute)
        time_since_added = str(time_since_added_date)

        # If error occur while parsing date, skip
        # TODO: handle case where date malformed (special string field)
        if not time_since_added_date:
            continue

        if not fetcher_footyroom.is_recent(time_since_added_date, max_days_ago):
            continue

        # Extract image link
        image = vid.find(class_='td-image-wrap')

        if not image:
            continue

        style = image.find("span").get("style")

        regex = "background-image: url\((.*?)\)"
        search_result = re.compile(regex, 0).search(style)

        img_link = ''

        if search_result:
            img_link = search_result.groups()[0]

        # Extract link
        link_tag = vid.find(class_="td-image-wrap")

        link = str(link_tag.get("href"))

        if not _is_valid_link(link):
            continue

        video_link = _get_video_link(link)

        if not video_link:
            continue

        highlights.append(HighlightsFootballHighlight(video_link, match_name, img_link, view_count, category, time_since_added))

    return highlights


def _is_valid_link(link):
    if not isinstance(link, str):
        return False

    # clean the URLS
    link = link.strip()

    # check if it is a football Match highlight video
    return link.startswith("https://highlightsfootball.com/video/")


def _get_video_link(full_link):
    page = requests.get(full_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    for iframe in soup.find_all("iframe"):
        src = iframe.get("src")

        # Only pick video urls coming from the following websites
        if src:
            if providers.DAILYMOTION in src:
                return format_dailymotion_link(src)

            if providers.STREAMABLE in src:
                return format_streamable_link(src)

            if providers.OK_RU in src:
                return format_link(src)

            if providers.MATCHAT_ONLINE in src:
                return format_link(src)

    return None


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights(num_pagelet=1)

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")