import requests
import time
from fb_bot.highlight_fetchers.info import providers


def check(link):
    """
    Check the validity of a link (if video is still available)

    :param link: the video link to check
    :return: True if the video is still available
    """

    if providers.DAILYMOTION in link:
        page = requests.get(link).text
        return not ('Content rejected.' in page or 'Content deleted.' in page)

    elif providers.STREAMABLE in link:
        page = requests.get(link).text
        return not ('Oops!' in page or "There's nothing here!" in page)

    elif providers.OK_RU in link:
        page = requests.get(link).text
        return not ('vp_video_stub_txt' in page or 'page-not-found' in page) # first is for content deleted, second for content not found

    elif providers.CONTENT_VENTURES in link \
            or providers.VIDEO_STREAMLET in link:
        page = requests.get(link).text.lower()
        return 'blocked Video' not in page

    elif providers.VEUCLIPS in link \
            or providers.VIUCLIPS in link \
            or providers.VIDSTREAM in link \
            or providers.TOCLIPIT in link:
        page = requests.get(link).text.lower()
        return not ('removed due to a copyright claim' in page
                    or 'video has been deleted' in page
                    or 'blocked Video' in page)

    # For all other content provider, return True by default
    return True


if __name__ == "__main__":

    print("\nHighlights check ------------------------------ \n")

    start_time = time.time()
    highlights = ['https://footy11.viuclips.net/embed/e5yXsPftKy'
                  ]

    for highlight in highlights:
        print(highlight + ' --> ' + str(check(highlight)))

    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")