import requests
import time


def check(link):
    """
    Check the validity of a link (if video is still available)

    :param link: the video link to check
    :return: True if the video is still available
    """

    page = requests.get(link).text

    # FIXME: improve performance by performing HEAD request
    if 'dailymotion' in link:
        return not ('Content rejected.' in page or 'Content deleted.' in page)

    elif 'streamable' in link:
        return not 'Oops!' in page

    else:
        # For all other content provider, return True by default
        return True


if __name__ == "__main__":

    print("\nHighlights check ------------------------------ \n")

    start_time = time.time()
    highlights = ['https://streamable.com/e/n3bpf', # True
                  'https://streamable.com/e/sstxd', # False
                  'http://www.dailymotion.com/embed/video/x6czbc8?start=0', # True
                  'http://www.dailymotion.com/embed/video/x6bm57o?start=18', # False
                  'http://www.dailymotion.com/embed/video/x6fnbfs'] # False

    for highlight in highlights:
        print(highlight + ' --> ' + str(check(highlight)))

    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")