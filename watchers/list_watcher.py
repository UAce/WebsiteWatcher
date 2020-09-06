import logging
from bs4 import BeautifulSoup, element

from config import config
from common.utils import send_email
from watchers.base_watcher import BaseWatcher

log = logging.getLogger(__name__)


class ListWatcher(BaseWatcher):
    name = "ListWatcher"

    def __init__(self, url: str, count: int, options: dict) -> None:
        super().__init__(url, options)
        self.initial_count = count
        self.current_count = self.initial_count
        self.list_tags = []

    def work(self):
        log.info(f'{self.name} working...')
        self.driver.get(self.url)
        target_page = self.driver.page_source

        soup = BeautifulSoup(target_page, 'html.parser')
        lists = soup.find_all(
            self.options['list_tag'], {
                self.options['list_attr']: self.options['list_attr_val']
            })

        if len(lists) > 1:
            raise Exception(f'More than one target list found.'
                            'Please select a unique list')
        elif len(lists) == 0:
            raise Exception('Target list not found')
        else:
            target_list = lists[0]

        current_count = self.find_count(
            target_list, self.options['target_tag'],
            self.options['target_attr'], self.options['target_attr_val'])
        if current_count != self.initial_count:
            log.info(f"Change detected. Number of items: {current_count}")
            self.current_count = current_count
            self.report()
            self.completed = True
        else:
            log.warn(
                f"No change detected. Retrying in {self.polling_interval}s...")

    def find_count(self, element: element.Tag, target: str, target_attr: str,
                   target_attr_val: str) -> None:
        print(target_attr, target_attr_val)
        children = element.findChildren()  # Finds all children recursively
        count = 0
        for i in range(len(children)):
            child = children[i]
            if child.has_attr(target_attr) and \
                    target_attr_val in child[target_attr] and \
                    child.name == target:
                log.info(f'found [{child.text}]')
                self.list_tags.append(child.text)
                count += 1
        return count

    def report(self, e: Exception = None) -> None:
        super().report(e)
        if e is None:
            items = '<br>- ' + '<br>- '.join(self.list_tags)
            content = f"""
            The list you are watching has changed!
            There are now {self.current_count} items.
            <br><br>
            {items}
            """

            send_email(f"{self.name} News!", content)
