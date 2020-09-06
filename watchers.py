import os
import time
import logging
from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import config
from common.utils import send_email

log = logging.getLogger(__name__)
polling_interval = config['watcher_settings']['polling_interval']


class BaseWatcher():
    name = "BaseWatcher"

    def __init__(self, url: str, options: dict) -> None:
        log.debug(f'init {self.name}')
        self.url = url
        self.options = options
        self.completed = False
        self.setup()

    def start(self) -> None:
        log.info(f'Starting {self.name}')
        try:
            while not self.completed:
                self.work()
                time.sleep(polling_interval)
        except Exception as e:
            self.driver.close()
            self.report(e)
            raise e

    def setup(self) -> None:
        log.info(f'Setting up {self.name}')
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path=os.path.abspath("chromedriver"),
            chrome_options=chrome_options)

    def work(self) -> None:
        log.info(f'{self.name} working...')
        self.driver.get(self.url)
        self.driver.get_screenshot_as_file('target_page.png')
        self.completed = True

    def report(self, e: Exception = None) -> None:
        if e is not None:
            log.error(f'An error occured when running {self.name}: {e}')
            send_email(f'{self.name} Error..', f'{e}')


class ListWatcher(BaseWatcher):
    name = "ListWatcher"

    def __init__(self, url: str, count: int, options: dict) -> None:
        super().__init__(url, options)
        self.initial_count = count
        self.current_count = self.initial_count
        self.list_elements = []

    def work(self):
        log.info(f'{self.name} working...')
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
        if current_count != self.initial_count:
            log.debug(
                f"Condition met: {current_count} != {self.initial_count}")
            self.current_count = current_count
            self.report()
            self.completed = True
        else:
            log.warn(f"Condition not met. Retrying in {polling_interval}s...")

    def find_count(self, element: element.Tag, target: str, target_attr: str,
                   target_attr_val: str):
        children = element.findChildren()  # Finds all children recursively
        count = 0
        for i in range(len(children)):
            child = children[i]
            if child.has_attr(target_attr) and \
                    target_attr_val in child[target_attr] and \
                    child.name == target:
                log.info(f'found [{child.text}]')
                self.list_elements.append(child.text)
                count += 1
        return count

    def report(self, e: Exception = None) -> None:
        super().report(e)
        if e is None:
            items = '<br>- ' + '<br>- '.join(self.list_elements)
            content = f"""
            The list you are watching has changed!
            There are now {self.current_count} items.
            <br><br>
            {items}
            """

            send_email(f"{self.name} News!", content)
