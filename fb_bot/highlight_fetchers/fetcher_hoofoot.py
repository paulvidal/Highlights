import time

import dateparser
import requests
from bs4 import BeautifulSoup

from fb_bot.highlight_fetchers import fetcher_footyroom
from fb_bot.highlight_fetchers.info import providers, sources
from fb_bot.highlight_fetchers.utils.Highlight import Highlight
from fb_bot.highlight_fetchers.utils.link_formatter import format_dailymotion_link, format_streamable_link, format_link

ROOT_URL = 'http://hoofoot.com/'
PAGELET_EXTENSION = '?page='


class HoofootHighlight(Highlight):

    def __init__(self, link, match_name, img_link, view_count, category, time_since_added):
        super().__init__(link, match_name, img_link, view_count, category, time_since_added, goal_data=[], type='normal')

    def get_match_info(self, match):
        match_split = match.split()
        middle_index = match_split.index('-')

        def join(l):
            return " ".join(l)

        team1 = join(match_split[:middle_index - 1])
        score1 = match_split[middle_index - 1]
        team2 = join(match_split[middle_index + 2:])
        score2 = match_split[middle_index + 1]

        return team1, score1, team2, score2

    def get_source(self):
        return sources.HOOFOOT


def fetch_highlights(num_pagelet=4, max_days_ago=7):
    """
    Fetch all the possible highlights available on hoofooot given a number of pagelet to look at
    (16 highlights per pagelet)

    :param num_pagelet: number of pagelet to consider
    :param max_days_ago: max age of a highlight (after this age, we don't consider the highlight)
    :return: the latests highlights available on hoofooot
    """

    highlights = []

    for pagelet_num in range(num_pagelet):
        highlights += _fetch_pagelet_highlights(pagelet_num + 1, max_days_ago)

    return highlights


def _fetch_pagelet_highlights(pagelet_num, max_days_ago):
    highlights = []

    page = requests.get(ROOT_URL + PAGELET_EXTENSION + str(pagelet_num))
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract videos
    for vid in soup.find_all(id="cocog"):

        # Extract link
        link_tag = vid.find("a")

        link = str(link_tag.get("href"))

        if not _is_valid_link(link):
            continue

        full_link = _form_full_link(link)
        video_link = _get_video_link(full_link)

        if not video_link:
            continue

        # Extract image link
        image = link_tag.find("img")

        if not image:
            continue

        img_link = str(image.get("src"))

        # Extract match name
        match_name = str(image.get("alt"))

        # Extract view count - NOT AVAILABLE for this website
        view_count = 0

        # Extract category
        info = vid.find(class_="info")

        if not info:
            continue

        info_img = info.find("img")

        if not info_img:
            continue

        category = str(info_img.get("alt"))

        # Extract time since video added
        info_font = info.find("font")

        if not info_font:
            continue

        time_since_added = str(info_font.get_text())
        time_since_added_date = dateparser.parse(time_since_added)

        # If error occur while parsing date, skip
        # TODO: handle case where date malformed (special string field)
        if not time_since_added_date:
            continue

        if not fetcher_footyroom.is_recent(time_since_added_date, max_days_ago):
            continue

        highlights.append(HoofootHighlight(video_link, match_name, img_link, view_count, category, time_since_added))

    return highlights


def _is_valid_link(link):
    if not isinstance(link, str):
        return False

    # clean the URLS
    link = link.strip()

    # check if it is a football Match highlight video
    return link.startswith("./?match=")


def _form_full_link(link):
    return ROOT_URL + link[2:]


def _get_video_link(full_link):
    page = requests.get(full_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    for iframe in soup.find_all("iframe"):
        src = iframe.get("src")

        if not src:
            continue

        # Only pick video urls coming from the following websites
        if providers.DAILYMOTION in src:
            return format_dailymotion_link(src)

        elif providers.STREAMABLE in src:
            return format_streamable_link(src)

        elif providers.MATCHAT_ONLINE in src:
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