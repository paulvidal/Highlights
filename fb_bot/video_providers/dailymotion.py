import re
from json import JSONDecodeError

import requests

from fb_bot.exceptions.TooManyRequestException import TooManyRequestsException
from fb_bot.highlight_fetchers.info import providers
from fb_bot.logger import logger

VIDEO_INFO_ENDPOINT = 'https://api.dailymotion.com/video/{}?fields=duration'


def get_video_info(link):

    # Make sure video is from Streamable
    if not providers.DAILYMOTION in link:
        return None

    # Get rid of any argument at end of video link
    link = re.compile('[?](.*)', 0).sub('', link)

    search_result = re.compile('/video/(.*)', 0).search(link)

    if not search_result:
        return None

    resource = search_result.groups()[0]

    json = None
    response = None

    try:
        response = requests.get(VIDEO_INFO_ENDPOINT.format(resource))
        json = response.json()
    except JSONDecodeError:
        logger.log('Dailymotion status: ' + str(response.status_code) + ' | Error url: ' + VIDEO_INFO_ENDPOINT.format(resource), forward=True)

        # TODO: check if dailymotion send too many requests error code
        if response.status_code == requests.codes.too_many_requests:
            raise TooManyRequestsException

    if not json or json.get('error'):
        return None

    info = {
        'duration': int(json['duration']),
        'video_url': None
    }

    return info


if __name__ == "__main__":
    print(get_video_info('http://www.dailymotion.com/embed/video/x6crigv?start=0'))