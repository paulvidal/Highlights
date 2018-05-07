from bs4 import BeautifulSoup
from raven.contrib.django.raven_compat.models import client, settings
from selenium.common.exceptions import NoSuchElementException

from fb_bot.highlight_fetchers.drivers.browser import Browser
from fb_bot.logger import logger


def get_video_info(link):

    # Make sure video is from matchat.online
    if not 'matchat.online' in link:
        return None

    browser = None
    response = None

    try:
        browser = Browser()
        browser.get(link)

        browser.wait(3)
        browser.click_on_element('.rmp-overlay-button')
        browser.wait(4)

        response = browser.get_html()

    except NoSuchElementException:
        return {
            'duration': -1,
            'video_url': None
        }

    except Exception:
        client.captureException()
        logger.log('matchat.online status: error | Error url: ' + link, forward=True)
        return None

    finally:
        if browser:
            browser.close()

    soup = BeautifulSoup(response, 'html.parser')
    duration = soup.find(class_="rmp-duration").get_text()

    if not ':' in duration:
        return None

    duration = duration.split(':')

    info = {
        'duration': int(duration[0]) * 60 + int(duration[1]),
        'video_url': None
    }

    return info


if __name__ == "__main__":
    print(get_video_info('https://hfoot.matchat.online/player/49641'))