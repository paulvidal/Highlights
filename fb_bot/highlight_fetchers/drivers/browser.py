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


if __name__ == "__main__":
    start_time = time.time()

    url = "https://hfoot.matchat.online/player/49641"

    b = Browser()
    b.get(url)
    b.wait(2)
    b.click_on_element('.rmp-overlay-button')
    b.wait(3)
    print(b.get_html())
    b.close()

    print("Time taken: " + str(round(time.time() - start_time, 2)) + "s")