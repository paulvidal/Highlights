import json
import time
from datetime import datetime

import dateparser
import nltk
import requests
from bs4 import BeautifulSoup

from fb_bot.highlight_fetchers import fetcher_footyroom
from fb_bot.highlight_fetchers.info import providers, sources
from fb_bot.highlight_fetchers.utils.Highlight import Highlight
from fb_bot.highlight_fetchers.utils.link_formatter import format_streamable_link, format_link, format_dailymotion_link

ROOT_URL = 'https://sportyhl.com/wp-admin/admin-ajax.php'


class SportyHLHighlight(Highlight):

    def __init__(self, link, match_name, img_link, view_count, category, time_since_added, type):
        super().__init__(link, match_name, img_link, view_count, category, time_since_added, goal_data=[], type=type)

    def get_match_info(self, match):
        match = match.split('Highlights')[0].strip()

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
        return sources.SPORTYHL


def fetch_highlights(num_pagelet=4, max_days_ago=15):
    """
    Fetch all the possible highlights available on sportyhl given a number of pagelet to look at
    (15 highlights per pagelet)

    :param num_pagelet: number of pagelet to consider
    :param max_days_ago: max age of a highlight (after this age, we don't consider the highlight)
    :return: the latests highlights available on sportyhl
    """

    highlights = []

    for pagelet_num in range(num_pagelet):
        highlights += _fetch_pagelet_highlights(pagelet_num + 1, max_days_ago)

    return highlights


def _fetch_pagelet_highlights(pagelet_num, max_days_ago):
    highlights = []

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[category]\"\r\n\r\n58,29,72,69,30,65,907,31,419,67,18,417,25,63,82,28,256\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[count]\"\r\n\r\n15\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[order_by]\"\r\n\r\ndate\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[order]\"\r\n\r\nDESC\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[style]\"\r\n\r\nlisting-classic\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[show_excerpt]\"\r\n\r\n0\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[cats-tags-condition]\"\r\n\r\nand\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[cats-condition]\"\r\n\r\nin\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[tags-condition]\"\r\n\r\nin\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[featured_image]\"\r\n\r\n0\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[ignore_sticky_posts]\"\r\n\r\n1\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[disable_duplicate]\"\r\n\r\n0\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[paginate]\"\r\n\r\nmore_btn\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[pagination-show-label]\"\r\n\r\n0\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[columns]\"\r\n\r\n3\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[override-listing-settings]\"\r\n\r\n0\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[_layout][state]\"\r\n\r\n1|1|1\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"query[_layout][page]\"\r\n\r\n1-col\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"view\"\r\n\r\nPublisher_Classic_Listing_1_Shortcode\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"current_page\"\r\n\r\n" \
              + str(pagelet_num) + "\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"_bs_pagin_token\"\r\n\r\n0060b77\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"action\"\r\n\r\npagination_ajax\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW--"

    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
    }

    page = requests.request("POST", ROOT_URL, data=payload, headers=headers)

    if page.text == 'INVALID TOKEN!':
        return []

    html = json.loads(page.text)['output'] \
        .replace("\n", "") \
        .replace("\t", "") \
        .replace("\\", "")

    soup = BeautifulSoup(html, 'html.parser')

    # Extract videos
    for vid in soup.find_all(class_='listing-inner'):

        # Extract match name
        match_name = str(vid.find(class_='title').find('a').get_text())

        if not 'vs' in match_name:
            # Check that the highlight is for a match
            continue

        # Extract view count - NOT AVAILABLE for this website
        view_count = 0

        # Extract category
        info = vid.find(class_='term-badge')

        if not info:
            continue

        category = str(info.find('a').get_text())

        # Extract time since video added
        date = vid.find(class_='post-meta').find('time')

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
        image = vid.find(class_='img-holder')

        if not image:
            continue

        img_link = image.get('data-src')

        # Extract link
        link_tag = vid.find(class_='img-holder').get('href')
        link = str(link_tag)

        if not _is_valid_link(link):
            continue

        video_links = _get_video_links(link)

        if not video_links:
            continue

        # Add multiple video links
        for type, link in video_links:
            highlights.append(SportyHLHighlight(link, match_name, img_link, view_count, category, time_since_added, type))

    return highlights


def _is_valid_link(link):
    if not isinstance(link, str):
        return False

    # clean the URLS
    link = link.strip()

    # check if it is a football Match highlight video
    return link.startswith("https://sportyhl.com/video")


def _get_video_links(full_link):
    video_links = []

    page = requests.get(full_link)
    soup = BeautifulSoup(page.text, 'html5lib')

    tab_mapping = []
    tabs = soup.find(class_='bs-tab-shortcode')

    for tab in tabs.find_all('li'):
        a = tab.find('a')
        type = a.get_text()
        id = a.get('href').replace('#', '')

        tab_mapping.append(
            (type, id)
        )

    for type, id in tab_mapping:

        for accepted in ['highlights', 'extended hl', 'moth hl', 'motd highlights']:
            # Do distance to be more robust against site typing errors
            if nltk.edit_distance(type.lower(), accepted) <= 2 or accepted in type.lower():

                # Get video type
                type = 'normal'

                if accepted in ['extended hl']:
                    type = 'extended'
                elif accepted in ['highlights', 'moth hl', 'motd highlights']:
                    type = 'normal'

                # Get the iframe
                div = soup.find(id=id)
                iframe = div.find('iframe') if div else None

                if not iframe:
                    continue

                src = iframe.get("src")

                # Only pick video urls coming from the following websites
                if src:
                    video_link = ''

                    if providers.DAILYMOTION in src:
                        video_link = format_dailymotion_link(src)

                    elif providers.STREAMABLE in src:
                        video_link = format_streamable_link(src)

                    elif providers.OK_RU in src:
                        video_link = format_link(src)

                    elif providers.MATCHAT_ONLINE in src:
                        video_link = format_link(src)

                    if video_link:
                        video_links.append(
                            (type, video_link)
                        )

    return video_links


if __name__ == "__main__":

    print("\nFetch highlights ------------------------------ \n")

    start_time = time.time()
    highlights = fetch_highlights(num_pagelet=4, max_days_ago=40)

    for highlight in highlights:
        print(highlight)

    print("Number of highlights: " + str(len(highlights)))
    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")