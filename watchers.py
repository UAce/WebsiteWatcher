import os
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import config

logger = logging.getLogger(__name__)
polling_interval = config['watcher_settings']['polling_interval']


class BaseWatcher():
    name = "BaseWatcher"

    def __init__(self, url: str, options: dict) -> None:
        logger.debug(f'init {self.name}')
        self.url = url
        self.options = options
        self.completed = False
        self.setup()

    def start(self) -> None:
        logger.info(f'Starting {self.name}')
        try:
            while not self.completed:
                self.work()
                time.sleep(polling_interval)
        except Exception as e:
            self.driver.close()
            print(e)
            raise e

    def setup(self) -> None:
        logger.info(f'Setting up {self.name}')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path=os.path.abspath("chromedriver"),
            chrome_options=chrome_options)

    def work(self) -> None:
        logger.info(f'{self.name} working...')
        self.driver.get(self.url)
        self.driver.get_screenshot_as_file('target_page.png')
        self.completed = True


class ListWatcher(BaseWatcher):
    name = "ListWatcher"

    def __init__(self, url: str, count: int, options: dict) -> None:
        super().__init__(url, options)
        self.count = count

    def work(self):
        logger.info(f'{self.name} working...')
        self.driver.get(self.url)
        target_page = self.driver.page_source

        soup = BeautifulSoup(target_page, 'html.parser')
        lists = soup.find_all(
            self.options.get('list_element'), {
                self.options.get('list_attr'):
                self.options.get('list_attr_val')
            })

        if len(lists) > 1:
            raise Exception(f'More than one target list found.'
                            'Please select a unique list')
        elif len(lists) == 0:
            raise Exception('Target list not found')
        else:
            target_list = lists[0]

        current_count = self.find_count(target_list,
                                        self.options.get('target_element'),
                                        self.options.get('target_attr'),
                                        self.options.get('target_attr_val'))
        if current_count != self.count:
            logger.debug(f"Condition met: {current_count} != {self.count}")
            # self.report() # send email notification
            self.completed = True
        else:
            logger.warn(
                f"Condition not met. Retrying in {polling_interval}s...")

    def find_count(self, element, target, target_attr, target_attr_val):
        children = element.findChildren()  # Finds all children recursively
        count = 0
        for i in range(len(children)):
            child = children[i]
            if child.has_attr(target_attr) and \
                    target_attr_val in child[target_attr] and \
                    child.name == target:
                logger.info(f'found [{child.text}]')
                count += 1
        return count
