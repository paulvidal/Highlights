import re
import requests

from fb_bot.logger import logger


def get_video_info(link):

    # Make sure video is from Ok.ru
    if not 'ok.ru' in link:
        return None

    response = None

    try:
        response = requests.get(link)
    except Exception:
        logger.log('Ok.ru status: error | Error url: ' + link, forward=True)
        return None

    duration_search_result = re.compile('duration\\\\&quot;:\\\\&quot;(.*?)\\\\&quot;', 0).search(response.text)

    if not duration_search_result:
        return None

    duration = duration_search_result.groups()[0]

    info = {
        'duration': int(duration),
        'video_url': None
    }

    return info


if __name__ == "__main__":
    print(get_video_info('https://ok.ru/videoembed/871972342374'))