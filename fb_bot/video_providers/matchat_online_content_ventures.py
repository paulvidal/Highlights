from bs4 import BeautifulSoup
from raven.contrib.django.raven_compat.models import client, settings
from selenium.common.exceptions import NoSuchElementException

from fb_bot.highlight_fetchers.drivers.browser import Browser
from fb_bot.highlight_fetchers.info import providers
from fb_bot.logger import logger


def get_video_info(link):

    # Make sure video is from matchat.online
    if not providers.MATCHAT_ONLINE in link and not providers.CONTENT_VENTURES in link:
        return None

    browser = None

    try:
        browser = Browser()
        browser.get(link)

        browser.wait(3)
        browser.click_on_element('.rmp-overlay-button')
        browser.wait(10)

        response = browser.get_html()

    except NoSuchElementException:
        return {
            'duration': -1,
            'video_url': None
        }

    except Exception:
        client.captureException()
        logger.log('matchat.online status: ERROR | url: ' + link, forward=True)
        return None

    finally:
        if browser:
            browser.close()

    soup = BeautifulSoup(response, 'html.parser')
    duration_text = soup.find(class_="rmp-duration").get_text()

    logger.log('response: ' + str(response), forward=True)
    logger.log('duration_text: ' + str(duration_text), forward=True)

    if not ':' in duration_text:
        return None

    duration_text_parts = duration_text.split(':')
    duration = int(duration_text_parts[0]) * 60 + int(duration_text_parts[1])

    info = {
        'duration': duration,
        'video_url': None
    }

    logger.log('matchat.online status: SUCCESS | url: ' + link + ' | duration: ' + str(duration), forward=True)

    return info


if __name__ == "__main__":
    print(get_video_info('https://hfoot.matchat.online/player/49641'))