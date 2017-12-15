import requests
import dateparser
import time

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

ROOT_URL = 'http://footyroom.com/'
PAGELET_EXTENSION = 'posts-pagelet?page='


class Highlight:
    def __init__(self, link, match_name, img_link, view_count, category, time_since_added):
        self.link = link
        self.match_name = match_name
        self.img_link = img_link
        self.view_count = view_count
        self.category = category
        self.time_since_added = time_since_added

        # Match information
        team1, score1, team2, score2 = self.get_match_info()
        self.team1 = team1
        self.score1 = score1
        self.team2 = team2
        self.score2 = score2

    def get_match_info(self):
        match = self.match_name
        match_split = match.split()
        middle_index = match_split.index('-')

        def join(l):
            return " ".join(l)

        return join(match_split[:middle_index - 1]), match_split[middle_index - 1], \
               join(match_split[middle_index + 2:]), match_split[middle_index + 1]

    def is_match_of(self, team):
        team = team.lower()
        return self.team1.lower().startswith(team) or self.team2.lower().startswith(team)

    def __str__(self):
        return str((self.link, self.match_name, self.team1, self.score1, self.team2, self.score2,
                    self.img_link, self.view_count, self.category, self.time_since_added))


def fetch_highlights_for_team(team):
    highlights = fetch_highlights(10, 60)
    latest_highlights_for_team = list(filter(lambda h: h.is_match_of(team), highlights))

    return latest_highlights_for_team


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

        if not _is_recent(time_since_added, max_days_ago):
            continue

        highlights.append(Highlight(link, match_name, img_link, view_count, category, time_since_added))

    return highlights


def _is_recent(date, max_days_ago):
    if not isinstance(date, str):
        return False

    today = datetime.today()
    date = dateparser.parse(date)

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


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights()

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")

    print("\nFetch highlights for team ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights_for_team("Arsenal")

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")