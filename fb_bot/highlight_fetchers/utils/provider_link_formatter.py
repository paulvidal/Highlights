from urllib.parse import urlparse

from fb_bot.highlight_fetchers.info import providers
from fb_bot.highlight_fetchers.utils import link_formatter
from fb_bot.logger import logger


def format_link(link_to_format):
    link = link_to_format

    if providers.DAILYMOTION in link:
        link = link_formatter.format_dailymotion_link(link)

    elif providers.STREAMABLE in link:
        link = link_formatter.format_streamable_link(link)

    elif providers.OK_RU in link:
        link = link_formatter.format_ok_ru_link(link)

    elif providers.MATCHAT_ONLINE in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.VIDEO_STREAMLET in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.VEUCLIPS in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.VIDSTREAM in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.TOCLIPIT in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.CLIPVENTURES in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.VIUCLIPS in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.TO_STREAMIT in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.UPCLIPS in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.VIDSFORU in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.VSTREAMEU in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.FORSTREAM in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.MYVIDONLINE in link:
        link = link_formatter.format_matchat_link(link)

    elif providers.YOUTUBE in link:
        link = link_formatter._format_link(link)

    elif providers.YOUTUBE in link:
        link = link_formatter._format_link(link)

    elif providers.RUTUBE in link:
        link = link_formatter._format_link(link)

    elif providers.MLSOCCER in link:
        link = link_formatter._format_link(link)

    else:
        # Not found case
        hostname = urlparse(link).hostname

        logger.warning('Unknown link format: {}'.format(link_to_format), extra={
            'hostname': hostname
        })

        link = None

    return link
