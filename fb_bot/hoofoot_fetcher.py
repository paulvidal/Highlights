import requests
import dateparser
import time

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

ROOT_URL = 'http://hoofoot.com/'
PAGELET_EXTENSION = '?page='


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

        if src and (src.startswith("https://vid.me/") or src.startswith("http://www.dailymotion.com/") or src.startswith("https://streamable.com/")):
            return src

    return None


def fetch_highlights(num_pagelet=3):
    highlights = []

    for i in range(1, num_pagelet + 1):

        page = requests.get(ROOT_URL + PAGELET_EXTENSION + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract videos
        for vid in soup.find_all(id="cocog"):

            # Extract link
            link = str(vid.find("a").get("href"))

            if not _is_valid_link(link):
                continue

            full_link = _form_full_link(link)

            video_link = _get_video_link(full_link)

            highlights.append(video_link)

    return highlights


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights()

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")