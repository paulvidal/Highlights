import re
from json import JSONDecodeError

import requests

from fb_bot.Exceptions.TooManyRequestException import TooManyRequestsException
from fb_bot.logger import logger

VIDEO_INFO_ENDPOINT =  'https://ajax.streamable.com/extract?url={}'


def get_video_info(link):

    # Make sure video is from Streamable
    if not 'streamable.com' in link:
        return None

    # Get rid of any argument at end of video link
    link = re.compile('[?](.*)', 0).sub('', link)

    search_result = re.compile('/e/(.*)', 0).search(link)

    if not search_result:
        return None

    resource = search_result.groups()[0]

    json = None
    response = None

    try:
        response = requests.get(VIDEO_INFO_ENDPOINT.format(resource))
        json = response.json()
    except JSONDecodeError:
        logger.log('Streamable status: ' + str(response.status_code) + ' | Error url: ' + VIDEO_INFO_ENDPOINT.format(resource), forward=True)

        if response.status_code == requests.codes.too_many_requests:
            raise TooManyRequestsException

    if not json or json.get('error'):
        return None

    video_url = str(json['url'])

    # Check if the video resource url is accessible
    if requests.head(video_url).status_code != requests.codes.ok:
        video_url = None

    info = {
        'duration': int(json['duration']),
        'video_url': video_url
    }

    return info


if __name__ == "__main__":
    print(get_video_info('https://streamable.com/e/o0q2j'))