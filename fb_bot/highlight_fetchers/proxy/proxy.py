import requests

from fb_bot.highlight_fetchers.proxy import scraper_api_key_manager
from requests.utils import quote

from fb_bot.logger import logger

SCRAPER_GET_URL = "https://api.scraperapi.com?key={}&url={}&render={}"
SCRAPER_POST_URL = "https://api.scraperapi.com?key={}&url={}"


def get(url, render=False):
    render = 'true' if render else 'false'

    for key in scraper_api_key_manager.get_scraper_api_keys():
        response = requests.get(
            SCRAPER_GET_URL.format(key.code, form_url(url), render)
        )

        if response.status_code == requests.codes.unauthorized:
            logger.warning('Scrapper API key invalid - you should remove it: ' + key.code)
            continue

        if response.status_code == requests.codes.forbidden:
            logger.warning('Scrapper API key too many requests: ' + key.code)
            scraper_api_key_manager.invalidate_key(key)
            continue

        if response.status_code == requests.codes.ok and not key.valid:
            logger.warning('Scrapper API key reset: ' + key.code)
            scraper_api_key_manager.validate_key(key)

        return response

    logger.critical('Scrapper API - all keys are invalid')


def post(url, data):
    for key in scraper_api_key_manager.get_scraper_api_keys():
        response = requests.post(
            SCRAPER_POST_URL.format(key.code, form_url(url)),
            data=data
        )

        if response.status_code == requests.codes.unauthorized:
            logger.warning('Scrapper API key invalid - you should remove it: ' + key.code)
            continue

        if response.status_code == requests.codes.forbidden:
            logger.warning('Scrapper API key too many requests: ' + key.code)
            scraper_api_key_manager.invalidate_key(key)
            continue

        if response.status_code == requests.codes.ok and not key.valid:
            logger.warning('Scrapper API key reset: ' + key.code)
            scraper_api_key_manager.validate_key(key)

        return response

    logger.critical('Scrapper API - all keys are invalid')


def form_url(url):
    return quote(url)