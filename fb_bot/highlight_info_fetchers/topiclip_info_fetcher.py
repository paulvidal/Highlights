import re

import requests
from raven.contrib.django.models import client

from fb_bot.highlight_fetchers.info import providers
from fb_bot.logger import logger


def get_video_info(link):

    if not providers.CLIPVENTURES in link \
            and not providers.TOCLIPIT in link\
            and not providers.UPCLIPS in link \
            and not providers.TO_STREAMIT in link:
        return None

    try:
        page = requests.get(link)

        regex = "src: \'(.*?0.m3u8)\'"
        streaming_link_search_result = re.compile(regex, 0).search(page.text)

        streaming_link = 'https://' + streaming_link_search_result.groups()[0].replace('//', '').replace('0.m3u8',
                                                                                                         '360p.m3u8')

        text = requests.get(streaming_link).text

        regex = "#EXTINF:(.*?),"
        durations_search_result = re.findall(regex, text)

        duration = int(sum([float(d) for d in durations_search_result]))

        info = {
            'duration': duration,
            'video_url': None
        }

        logger.info('topiclip SUCCESS | url: ' + link + ' | duration: ' + str(duration))

        return info

    except:
        client.captureException()
        logger.error("Failed to fetch info for link {}".format(link))

        return {
            'duration': 0,  # Allow for retries if link is valid but scrapping not working
            'video_url': None
        }


if __name__ == '__main__':
    get_video_info('https://footy11.clipventures.com/embed/rGcLFVx5l3')
    get_video_info('https://hofoot.toclipit.com/embed/D5ayRenIHS')
    get_video_info('https://oms.upclips.online/embed/pAFPCGQYYF')