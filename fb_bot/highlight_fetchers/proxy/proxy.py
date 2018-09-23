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
            logger.log('Scrapper API key invalid - removing: ' + key.code, forward=True)
            scraper_api_key_manager.remove_key(key)
            continue

        if response.status_code == requests.codes.forbidden:
            logger.log('Scrapper API key too many requests: ' + key.code, forward=True)
            scraper_api_key_manager.invalidate_key(key)
            continue

        if response.status_code == requests.codes.ok and not key.valid:
            logger.log('Scrapper API key reset: ' + key.code, forward=True)
            scraper_api_key_manager.validate_key(key)

        return response


def post(url, data):
    for key in scraper_api_key_manager.get_scraper_api_keys():
        response = requests.post(
            SCRAPER_POST_URL.format(key.code, form_url(url)),
            data=data
        )

        if response.status_code == requests.codes.unauthorized:
            logger.log('Scrapper API key invalid - removing: ' + key.code, forward=True)
            scraper_api_key_manager.remove_key(key)
            continue

        if response.status_code == requests.codes.forbidden:
            logger.log('Scrapper API key too many requests: ' + key.code, forward=True)
            scraper_api_key_manager.invalidate_key(key)
            continue

        if response.status_code == requests.codes.ok and not key.valid:
            logger.log('Scrapper API key reset: ' + key.code, forward=True)
            scraper_api_key_manager.validate_key(key)

        return response


def form_url(url):
    return quote(url)