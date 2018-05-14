import random
import re
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup

from fb_bot.logger import logger
from highlights import settings

ACCOUNTS = [
    'tester@hotmail.fr',
    'tester2@hotmail.fr',
    'tester3@hotmail.fr',
    'tester4@hotmail.fr',
    'highlights@hotmail.fr',
    'highlights2@hotmail.fr',
    'highlights3@hotmail.fr',
    'highlights4@hotmail.fr',
]


def convert(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')

    for script in soup.find_all('script'):
        script_text = script.text

        if 'settings.bitrates' in script_text:
            regex = "settings.bitrates = {hls:\"//(.*?)\"}"
            search_result = re.compile(regex, 0).search(script_text)

            video_link = 'http://' + search_result.groups()[0]

            params = (
                ('url', video_link),
            )

            account = random.choice(ACCOUNTS)

            response = requests.get('https://api.streamable.com/import',
                                    params=params,
                                    auth=(account, settings.get_env_var('STREAMABLE_PASSWORD')))

            try:
                shortcode = response.json().get('shortcode')
            except JSONDecodeError:
                logger.log('Failed to create streamable video for: ' + url + ' | error: ' + response.text, forward=True)
                return None

            if shortcode:
                link = 'https://streamable.com/e/' + shortcode
                logger.log('New streamable video: ' + link + ' | for account: ' + account, forward=True)

                return link

    return None