import logging
import collections
import re
from selenium.webdriver.common.by import By
import time

from websiteWatcher.common.utils import send_email
from websiteWatcher.watchers.base_watcher import BaseWatcher

log = logging.getLogger(__name__)

collections.Callable = collections.abc.Callable
collections.MutableMapping = collections.abc.MutableMapping


class PriceWatcher(BaseWatcher):
    name = "PriceWatcher"

    def __init__(self, url: str, options: dict) -> None:
        super().__init__(url, options)
        self.initial_price: float = self.options["initial_price"]
        self.displayed_price: float = self.options["initial_price"]
        self.description = self.options["description"]

    def work(self):
        log.info(f"{self.name} working...")

        # reset state
        self.reset_state()

        # Load url and wait for page to load before parsing the HTML
        self.driver.get(self.url)
        log.info("Waiting for page to load...")
        time.sleep(5)  # wait for page to load
        price_str = self.driver.find_element(By.XPATH, self.options["full_xpath"]).text

        if (price_str is None):
            self.report(Exception("Price element not found"))
            self.completed = True

        # Parse price string and convert to float
        self.displayed_price = float(re.sub(r'[^0-9.]+', '', price_str))

        if (self.options['notify_on_change'] and self.displayed_price != self.initial_price):
            log.info(f"Price change detected. New Price: {self.displayed_price}")

            self.price_change_detected = True
            self.report()
            self.initial_price = self.displayed_price
            self.completed = self.options['stop_on_completion']
            return

        # If threshold price is not defined, return early
        if (self.options['threshold_price'] is None):
            return
        else:
            log.warn(
                f"Current price: ${self.displayed_price}. No price change detected. Retrying in {self.polling_interval}s...")

        is_threshold_higher = self.options['threshold_price'] > self.options['initial_price']
        is_threshold_reached = self.displayed_price >= self.options[
            'threshold_price'] if is_threshold_higher else self.displayed_price <= self.options['threshold_price']
        if (is_threshold_reached):
            log.info(f"Price reached threshold price! New Price: {self.displayed_price}")

            self.price_threshold_reached = True
            self.report()
            self.initial_price = self.displayed_price
            self.completed = self.options['stop_on_completion']
        else:
            log.warn(f"No price change detected. Retrying in {self.polling_interval}s...")

    def report(self, e: Exception = None) -> None:
        super().report(e)
        self.take_screenshot()
        if e is None:
            reason = "Price change detected" if self.price_change_detected else "Price reached threshold price"
            content = f"""
            <table
                role="presentation"
                border="0"
                cellpadding="0"
                cellspacing="0"
                class="body"
                >
                <tr>
                    <td class="container">
                    <div class="content">
                        <!-- START CENTERED WHITE CONTAINER -->
                        <table role="presentation" class="main">
                        <!-- START MAIN CONTENT AREA -->
                        <tr>
                            <td class="wrapper">
                            <table
                                role="presentation"
                                border="0"
                                cellpadding="0"
                                cellspacing="0"
                            >
                                <tr>
                                <td>
                                    <span style="font-weight: bold; font-size: 16px; color: red">${self.initial_price}</span> 
                                    <span style="font-weight: bold; font-size: 32px; color: white">→</span> 
                                    <span style="font-weight: bold; font-size: 16px; color: green">${self.displayed_price}</span> 
                                    <table
                                    role="presentation"
                                    border="0"
                                    cellpadding="0"
                                    cellspacing="0"
                                    style="margin-top: 16px;"
                                    >
                                    <tbody>
                                        <tr>
                                        <td align="left">
                                            <table
                                            role="presentation"
                                            border="0"
                                            cellpadding="0"
                                            cellspacing="0"
                                            style="height: 40px; background-color: #2f55ff; border-radius: 4px;"
                                            >
                                            <tbody>
                                                <tr>
                                                <td>
                                                    <a
                                                    href="{self.url}"
                                                    target="_blank"
                                                    style="color: white; font-weight: bold; text-decoration: none; cursor: pointer; padding: 16px;"
                                                    >Check out the new price!</a
                                                    >
                                                </td>
                                                </tr>
                                            </tbody>
                                            </table>
                                        </td>
                                        </tr>
                                    </tbody>
                                    </table>
                                </td>
                                </tr>
                            </table>
                            </td>
                        </tr>
                        <!-- END MAIN CONTENT AREA -->
                        </table>
                        <!-- END CENTERED WHITE CONTAINER -->
                    </div>
                    </td>
                </tr>
            </table>
            """

            send_email(f"{reason}! ({self.description})", content)

    def take_screenshot(self):
        self.driver.get_screenshot_as_file("images/Price-watcher-page.png")
        # body = self.driver.find_element(By.TAG_NAME, 'body')
        # left = int(body.location["x"])
        # top = int(body.location["y"])
        # right = int(body.location["x"] + body.size["width"])
        # bottom = int(body.location["y"] + body.size["height"])
        # im = Image.open("images/Price-watcher-page.png")
        # im = im.crop((left, top, right, bottom))
        # im.save("images/Price-watcher-cropped.png")

    def reset_state(self):
        self.price_change_detected = False
        self.price_threshold_reached = False
