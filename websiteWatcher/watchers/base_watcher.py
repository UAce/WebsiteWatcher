import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from websiteWatcher.settings.config import config
from websiteWatcher.common.utils import send_email

log = logging.getLogger(__name__)


class BaseWatcher:
    name = "BaseWatcher"

    def __init__(self, url: str, options: dict) -> None:
        log.debug(f"init {self.name}")
        self.url = url
        self.options = options
        self.completed = False
        self.setup()
        self.polling_interval = (
            self.options["polling_interval"]
            or config["watcher_settings"]["polling_interval"]
        )

    def start(self) -> None:
        log.info(f"Starting {self.name}")
        try:
            while not self.completed:
                self.work()
                time.sleep(self.polling_interval)
        except Exception as e:
            self.driver.close()
            self.report(e)
            raise e

    def setup(self) -> None:
        log.info(f"Setting up {self.name}")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path=os.path.abspath("chromedriver"),
            chrome_options=chrome_options,
        )

    def work(self) -> None:
        log.info(f"{self.name} working...")
        self.driver.get(self.url)
        self.driver.get_screenshot_as_file("target_page.png")
        self.completed = True

    def report(self, e: Exception = None) -> None:
        if e is not None:
            log.error(f"An error occured when running {self.name}: {e}")
            send_email(f"{self.name} Error..", f"{e}")
