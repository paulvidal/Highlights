import requests
import time

from fb_bot.highlight_fetchers.drivers.browser import Browser


def check(link):
    """
    Check the validity of a link (if video is still available)

    :param link: the video link to check
    :return: True if the video is still available
    """

    if 'dailymotion' in link:
        page = requests.get(link).text
        return not ('Content rejected.' in page or 'Content deleted.' in page)

    elif 'streamable' in link:
        page = requests.get(link).text
        return not 'Oops!' in page

    elif 'ok.ru' in link:
        page = requests.get(link).text
        return not ('vp_video_stub_txt' in page or 'page-not-found' in page) # first is for content deleted, second for content not found

    elif 'matchat.online' in link:
        page = None
        browser = None

        try:
            browser = Browser()
            page = browser.get(link).get_html()
        finally:
            if browser:
                browser.close()

        return not 'rmp-no-play-text' in page

    # For all other content provider, return True by default
    return True


if __name__ == "__main__":

    print("\nHighlights check ------------------------------ \n")

    start_time = time.time()
    highlights = ['https://streamable.com/e/n3bpf', # True
                  'https://streamable.com/e/sstxd', # False
                  'https://www.dailymotion.com/embed/video/x6icolk	', # True
                  'http://www.dailymotion.com/embed/video/x6bm57o?start=18', # False
                  'http://www.dailymotion.com/embed/video/x6fnbfs', # False
                  'https://ok.ru/videoembed/87798dafad', # False
                  'https://ok.ru/videoembed/877984746086', # False
                  'https://ok.ru/videoembed/703334517448', # True
                  'https://ok.ru/videoembed/871972342374',  # True
                  'https://hfoot.matchat.online/player/49500354',  # False
                  'https://hfoot.matchat.online/player/49422',  # True
                  'https://footy1.matchat.online/player/49639',  # True
                  ]

    for highlight in highlights:
        print(highlight + ' --> ' + str(check(highlight)))

    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")