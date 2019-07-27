import re
import requests
from raven.contrib.django.models import client

from fb_bot import ressource_checker
from fb_bot.highlight_fetchers.info import providers
from fb_bot.logger import logger
from fb_bot.model_managers import scrapping_status_manager


def get_video_info(link):

    # Make sure video is from matchat.online or videostreamlet.net
    if not providers.MATCHAT_ONLINE in link \
            and not providers.CONTENT_VENTURES in link \
            and not providers.VIDEO_STREAMLET in link \
            and not providers.VEUCLIPS in link\
            and not providers.VIUCLIPS in link:
        return None

    # Disable temporarily matchat.online as not working anymore
    if providers.MATCHAT_ONLINE in link or providers.CONTENT_VENTURES in link:
        return None

    try:
        page = requests.get(link)

        regex = "settings.bitrates = {hls:\"(.*?)\""
        streaming_link_search_result = re.compile(regex, 0).search(page.text)

        streaming_link = 'https://' + streaming_link_search_result.groups()[0].replace('//', '').replace('0.m3u8', '360p.m3u8')

        text = requests.get(streaming_link).text

        regex = "#EXTINF:(.*?),"
        durations_search_result = re.findall(regex, text)

        duration = int(sum([float(d) for d in durations_search_result]))

        info = {
            'duration': duration,
            'video_url': None
        }

        scrapping_status_manager.update_scrapping_status('m3u8', True)
        logger.info('matchat.online SUCCESS | url: ' + link + ' | duration: ' + str(duration))

        return info

    except:
        client.captureException()
        logger.error("Failed to fetch info for link {}".format(link))

        try:
            if ressource_checker.check(link):
                scrapping_status_manager.update_scrapping_status('m3u8', False)
                logger.error('matchat.online FAILURE | url: ' + link)

                return {
                    'duration': 0,  # Allow for retries if link is valid but scrapping not working
                    'video_url': None
                }

            else:
                return None

        except:
            client.captureException()
            logger.error("Failed to fetch info for link {} and resource check failed".format(link))

            return {
                'duration': 0,  # Allow for retries if link is valid but scrapping not working
                'video_url': None
            }