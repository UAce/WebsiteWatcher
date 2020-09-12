import logging
from PIL import Image
from bs4 import BeautifulSoup, element

from websiteWatcher.common.utils import send_email
from websiteWatcher.watchers.base_watcher import BaseWatcher

log = logging.getLogger(__name__)


class ListWatcher(BaseWatcher):
    name = "ListWatcher"

    def __init__(self, url: str, options: dict) -> None:
        super().__init__(url, options)
        self.initial_count = None
        self.current_count = self.initial_count
        self.list_items = []

    def work(self):
        log.info(f"{self.name} working...")
        self.driver.get(self.url)
        target_page = self.driver.page_source

        soup = BeautifulSoup(target_page, "html.parser")
        lists = soup.find_all(
            self.options["list_tag"],
            {self.options["list_attr"]: self.options["list_attr_val"]},
        )
        target_list = self.validate_target_list(lists)

        self.current_count = self.find_count(
            target_list,
            self.options["target_tag"],
            self.options["target_attr"],
            self.options["target_attr_val"],
        )
        self.take_screenshot()
        if self.initial_count is None:
            self.initial_count = self.current_count
        if self.current_count != self.initial_count:
            log.info(f"Change detected. Number of items: {self.current_count}")
            self.initial_count = self.current_count
            self.report()
            # self.completed = True
        else:
            log.warn(f"No change detected. Retrying in {self.polling_interval}s...")

    def find_count(
        self, element: element.Tag, target: str, target_attr: str, target_attr_val: str
    ) -> None:
        children = element.findChildren()  # Finds all children recursively
        count = 0
        new_list_items = []
        for i in range(len(children)):
            child = children[i]
            if (
                child.has_attr(target_attr)
                and target_attr_val in child[target_attr]
                and child.name == target
            ):
                log.info(f"found [{child.text}]")
                isNew = "(NEW)" if child.text in self.list_items else ""
                new_list_items.append(f"{child.text} {isNew}")
                count += 1
        self.list_items = new_list_items
        return count

    def validate_target_list(self, lists: list) -> element.Tag:
        if len(lists) > 1:
            raise Exception(
                "More than one target list found." "Please select a unique list"
            )
        elif len(lists) == 0:
            raise Exception("Target list not found")
        else:
            return lists[0]

    def report(self, e: Exception = None) -> None:
        super().report(e)
        if e is None:
            items = "<br>- " + "<br>- ".join(self.list_items)
            content = f"""
            The list you are watching has changed!
            There are now {self.current_count} items.
            <br><br>
            {items}
            <br><br>
            <a href="{self.url}">View the website</a>
            """

            send_email(f"{self.name} News!", content)

    def take_screenshot(self):
        list_tag = self.options["list_tag"]
        list_attr = self.options["list_attr"]
        list_attr_val = self.options["list_attr_val"]
        target_list = self.driver.find_element_by_xpath(
            f"//{list_tag}[contains(@{list_attr}, '{list_attr_val}')]"
        )

        if target_list.is_displayed():
            self.driver.get_screenshot_as_file("images/list-watcher-page.png")
            left = int(target_list.location["x"])
            top = int(target_list.location["y"])
            right = int(target_list.location["x"] + target_list.size["width"])
            bottom = int(target_list.location["y"] + target_list.size["height"])
            im = Image.open("images/list-watcher-page.png")
            im = im.crop((left, top, right, bottom))
            im.save("images/list-watcher-target.png")
