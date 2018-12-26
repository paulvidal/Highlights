import time

import os
from selenium import webdriver

from highlights.settings import BASE_DIR, DEBUG


class Browser:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.binary_location = "/app/.apt/usr/bin/google-chrome-stable"

        self.driver = webdriver.Chrome(executable_path=os.path.join(BASE_DIR, 'fb_bot/highlight_fetchers/drivers/chromedriver_mac'), chrome_options=chrome_options) if DEBUG else \
                      webdriver.Chrome(chrome_options=chrome_options)

    def get(self, url):
        self.driver.get(url)
        return self

    def click_on_element(self, selector):
        self.driver.find_element_by_css_selector(selector).click()
        return self

    def get_html(self):
        return self.driver.page_source

    def wait(self, seconds):
        time.sleep(seconds)
        return self

    def close(self):
        self.driver.close()