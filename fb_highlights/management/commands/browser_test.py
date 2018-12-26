import time

from bs4 import BeautifulSoup

from fb_bot.highlight_fetchers.drivers.browser import Browser
from fb_highlights.management.commands.CustomCommand import CustomCommand


class Command(CustomCommand):

    def get_task_name(self, options):
        return 'browser test'

    def run_task(self, options):
        start_time = time.time()

        url = "https://oms.matchat.online/embed/fwFkMv76Zm"

        b = Browser()
        b.get(url)
        b.wait(2)
        b.click_on_element('.rmp-overlay-button')
        b.wait(3)
        print(b.get_html())

        soup = BeautifulSoup(b.get_html(), 'html.parser')
        duration = soup.find(class_="rmp-duration").get_text()

        if b:
            b.close()

        if not ':' in duration:
            return None

        duration = duration.split(':')

        info = {
            'duration': int(duration[0]) * 60 + int(duration[1]),
            'video_url': None
        }

        print(info)

        print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")