from config import config
import logging

from watchers import ListWatcher, BaseWatcher
from common.logger_utils import color_formatter, default_formatter

logger = logging.getLogger(__name__)


def configure_logger(watcher: BaseWatcher) -> None:
    console = logging.StreamHandler()
    console.setFormatter(color_formatter)
    log_file = logging.FileHandler(
        filename=f"{config['log_dir']}/{watcher.name}.log")
    log_file.setFormatter(default_formatter)
    logging.basicConfig(
        level=config['log_level'], handlers=[console, log_file])


def main() -> None:
    target_url = "https://www.petfinder.com/search/cats-for-adoption/ca/quebec/montreal/?age%5B0%5D=Baby&distance=10&gender%5B0%5D=female"
    initial_count = 5
    options = dict(
        list_element='pfdc-animal-search-results',
        list_attr='observe-state',
        list_attr_val='animalSearch.results',
        target_element='span',
        target_attr='data-test',
        target_attr_val='Pet_Card_Pet_Details_List')

    cw = ListWatcher(target_url, initial_count, options)
    configure_logger(cw)
    cw.start()


if __name__ == "__main__":
    print('Running main...')
    main()
