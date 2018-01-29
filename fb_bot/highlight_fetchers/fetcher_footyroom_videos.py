import re

import requests
import dateparser
import time
from fb_bot.highlight_fetchers.Highlight import Highlight

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

ROOT_URL = 'http://footyroom.com/'
PAGELET_EXTENSION = 'posts-pagelet?page='


class FootyroomVideoHighlight(Highlight):

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
        return 'footyroom_video'


def fetch_highlights(num_pagelet=3, max_days_ago=7):
    """
    Fetch all the possible highlights available on footyroom given a number of pagelet to look at
    (24 highlights per pagelet)

    :param num_pagelet: number of pagelet to consider
    :param max_days_ago: max age of a highlight (after this age, we don't consider the highlight)
    :return: the latests highlights available on footyroom
    """

    highlights = []

    for pagelet_num in range(num_pagelet):
        highlights += _fetch_pagelet_highlights(pagelet_num + 1, max_days_ago)

    return highlights


def _fetch_pagelet_highlights(pagelet_num, max_days_ago):
    highlights = []

    page = requests.get(ROOT_URL + PAGELET_EXTENSION + str(pagelet_num))
    soup = BeautifulSoup(page.content, 'html.parser')

    for video_card in soup.find_all(class_="card"):

        # Get link of video
        video = video_card.find(class_="card-image")

        if video is None or video.find("a") is None:
            continue

        link = str(video.find("a").get("href"))

        if not _is_valid_link(link):
            continue

        full_link = _form_full_link(link)
        video_link = _get_video_link(full_link)

        if not video_link:
            print(full_link)
            continue

        # Get match image link
        img_link = str(video.find("img").get("src"))

        # Get video view count
        video_info = video.find(class_="card-info")
        view_count = 0

        if video_info and video_info.find(class_="views-count"):
            view_count = int(video_info.find(class_="views-count").get_text())

        # Get match name
        title = video_card.find(class_="card-title")

        if not title:
            continue

        match_name = str(title.find(class_="spoiler").get_text())

        # Get category
        vid_category = video_card.find(class_="card-category")
        category = ""

        if vid_category:
            category = vid_category.get_text()

        # Get time since video added
        vid_time_added = video_card.find(class_="card-time")

        if vid_time_added is None:
            continue

        time_since_added = str(vid_time_added.get_text())
        time_since_added_date = dateparser.parse(time_since_added)

        # If error occur while parsing date, skip
        # TODO: handle case where date malformed (special string field)
        if not time_since_added_date:
            continue

        if not _is_recent(time_since_added_date, max_days_ago):
            continue

        highlights.append(FootyroomVideoHighlight(video_link, match_name, img_link, view_count, category, time_since_added))

    return highlights


def _is_recent(date, max_days_ago):
    if not isinstance(date, datetime):
        return False

    today = datetime.today()

    # Return True if the video is less than a week old
    return (today - date) < timedelta(days=max_days_ago)


def _is_valid_link(link):
    if not isinstance(link, str):
        return False

    # clean the URLS
    link = link.strip()
    link = link[len(ROOT_URL):]

    # check if it is a football Match highlight video
    return link.startswith("matches/") and link.endswith("/review")


def _form_full_link(link):
    return link


def _get_video_link(full_link):
    page = requests.get(full_link)
    soup = BeautifulSoup(page.content, 'html.parser')

    for script in soup.find_all('script'):
        script_text = script.text

        if 'dailymotion' in script_text:
            regex = 'src=\\\\"\\\/\\\/(www.dailymotion.com\\\/embed\\\/video\\\/.*?)\\\"'
            search_result = re.compile(regex, 0).search(script_text)

            if not search_result:
                return None

            link = search_result.groups()[0].replace('\\', '')

            return 'https://' + link

        elif 'streamable' in script_text:
            regex = 'src=\\\\"(https:\\\/\\\/streamable.com.*?)\\"'
            search_result = re.compile(regex, 0).search(script_text)

            if not search_result:
                return None

            link = search_result.groups()[0].replace('\\', '')
            base_url = link.split('/s/')[0]
            resource_id = link.split('/s/')[1].split('/')[0]

            # Return streamable link in the format 'https://streamable.com/e/ioz1l'
            return base_url + '/e/' + resource_id

        elif 'ok.ru' in script_text:
            regex = 'src=\\\\"\\\/\\\/(ok.ru.*?)\\\"'
            search_result = re.compile(regex, 0).search(script_text)

            if not search_result:
                return None

            link = search_result.groups()[0].replace('\\', '')

            return 'https://' + link

        elif 'youtube' in script_text:
            regex = 'src=\\\\"(https:\\\/\\\/www.youtube.com.*?)\\\"'
            search_result = re.compile(regex, 0).search(script_text)

            if not search_result:
                return None

            link = search_result.groups()[0].replace('\\', '')

            return link

        elif 'rutube.ru' in script_text:
            regex = 'src=\\\\"\\\/\\\/(rutube.ru.*?)\\\"'
            search_result = re.compile(regex, 0).search(script_text)

            if not search_result:
                return None

            link = search_result.groups()[0].replace('\\', '')

            return 'https://' + link

    return None


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights()

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")
