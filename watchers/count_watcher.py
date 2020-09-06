from bs4 import BeautifulSoup

from base_watcher import BaseWatcher


class CountWatcher(BaseWatcher):
    def __init__(self, url, count, options):
        self.url = url
        self.count = count
        self.options = options
        self.completed = False
        self.setup()

    def start(self):
        try:
            while not self.completed:
                self.work()
        except Exception as e:
            self.driver.close()
            print(e)
            raise e

    def work(self):
        self.driver.get(self.url)
        target_page = self.driver.page_source

        soup = BeautifulSoup(target_page, 'html.parser')
        lists = soup.find_all(
            self.options.list_element, {
                self.options.list_attr: self.options.list_attr_val
            })

        if len(lists) > 1:
            raise Exception(f'More than one target list found.'
                            'Please select a unique list')
        elif len(lists) == 0:
            raise Exception('Target list not found')
        else:
            target_list = lists[0]

        current_count = self.find_count(
            target_list, self.options.target_element, self.options.target_attr,
            self.options.target_attr_val)
        if current_count != self.count:
            # self.report() # send email notification
            self.completed = True

    def find_count(self, element, target, target_attr, target_attr_val):
        children = element.findChildren()  # Finds all children recursively
        count = 0
        for i in range(len(children)):
            child = children[i]
            if child.has_attr(target_attr) and \
                    target_attr_val in child[target_attr] and \
                    child.name == target:
                print(f'{child.text}')
                count += 1

        return count
