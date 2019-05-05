from fb_bot.exceptions.TooManyRequestException import TooManyRequestsException
from fb_bot.logger import logger
from fb_bot.highlight_info_fetchers import dailymotion_info_fetcher, ok_ru_info_fetcher, streamable_info_fetcher, matchat_online_info_fetcher

ALL_VIDEO_INFO_FETCHER = [
    {
        'name': 'dailymotion',
        'fetch': dailymotion_info_fetcher.get_video_info
    },
    {
        'name': 'streamable',
        'fetch': streamable_info_fetcher.get_video_info
    },
    {
        'name': 'ok.ru',
        'fetch': ok_ru_info_fetcher.get_video_info
    },
    {
        'name': 'matchat.online',
        'fetch': matchat_online_info_fetcher.get_video_info
    }
]


def get_info(link):
    """
    Find the video info for video link

    :param link: the video link
    :return: the info of the video (duration, ressource url)
    """

    for fetcher in ALL_VIDEO_INFO_FETCHER:
        info = None

        try:
            info = fetcher['fetch'](link)

        except TooManyRequestsException:

            # remove temporarily fetcher for which too many request
            for fetcher_from_list in ALL_VIDEO_INFO_FETCHER:

                if fetcher['name'] == fetcher_from_list['name']:
                    logger.log('REMOVING fetcher: ' + fetcher['name'], forward=True)
                    ALL_VIDEO_INFO_FETCHER.remove(fetcher_from_list)

        if info:
            return info

    return None
