import requests
import dateparser

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

ROOT_URL = 'http://footyroom.com/'


class Highlight:

    def __init__(self, link, match_name, img_link, view_count, category, time_since_added):
        self.link = link
        self.match_name = match_name
        self.img_link = img_link
        self.view_count = view_count
        self.category = category
        self.time_since_added = time_since_added

    def __str__(self):
        return str((self.link, self.match_name, self.img_link, self.view_count, self.category, self.time_since_added))


def fetch_highlights():
    highlights = []

    page = requests.get(ROOT_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    for vid in soup.find_all(class_="vid"):
        # Get link of video
        vid_top = vid.find(class_="vidTop")

        if vid_top is None:
            continue

        link = str(vid_top.find("a").get("href"))

        if not _is_valid_link(link):
            continue

        # Get match name
        match_name = vid_top.find("a").get_text()

        # Get match image link
        vid_thumb = vid.find(class_="vidthumb")
        img_link = str(vid_thumb.find("img").get("src"))

        # Get video view count
        vid_bot = vid.find(class_="vidBot")
        view_count = int(vid_bot.find(class_="views-count").get_text())

        # Get category
        vid_category = vid.find(class_="vid_category")
        category = vid_category.find("a").get_text()

        # Get time since video added
        vid_time_added = vid.find(class_="time_added")
        time_since_added = vid_time_added.get_text()

        if not _is_recent(time_since_added):
            continue

        highlights.append(Highlight(link, match_name, img_link, view_count, category, time_since_added))

    return highlights


def _is_recent(date):
    if not isinstance(date, str):
        return False

    today = datetime.today()
    date = dateparser.parse(date)

    # Return True if the video is less than a week old
    return (today - date) < timedelta(days=7)


def _is_valid_link(link):
    if not isinstance(link, str):
        return False

    # clean the URLS
    link = link.strip()
    link = link[len(ROOT_URL):]

    # check if it is a football Match highlight video
    return link.startswith("matches/") and link.endswith("/review")


if __name__ == "__main__":

    for highlight in fetch_highlights():
        print(highlight)
