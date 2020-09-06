import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseWatcher():
    def __init__(self, url, options):
        self.url = url
        self.options = options
        self.completed = False
        self.setup()

    def watch(self):
        try:
            while not self.completed:
                self.work()
        except Exception as e:
            self.driver.close()
            print(e)
            raise e

    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path=os.path.abspath("chromedriver"),
            chrome_options=chrome_options)

    def work(self):
        self.driver.get(self.url)
        self.driver.get_screenshot_as_file('target_page.png')
        self.completed = True
