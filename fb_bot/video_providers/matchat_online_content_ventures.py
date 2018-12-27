import re
import requests

from fb_bot.highlight_fetchers.info import providers
from fb_bot.logger import logger


def get_video_info(link):

    # Make sure video is from matchat.online
    if not providers.MATCHAT_ONLINE in link and not providers.CONTENT_VENTURES in link:
        return None

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

    logger.log('matchat.online INFO | url: ' + link + ' | duration: ' + str(duration), forward=True)

    return info
