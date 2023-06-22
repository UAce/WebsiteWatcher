import logging
import sys

from websiteWatcher.common.utils import configure_logger, parse_arguments
from websiteWatcher.watchers.list_watcher import ListWatcher
from websiteWatcher.watchers.price_watcher import PriceWatcher


def main() -> None:
    args = parse_arguments()
    watcher = None
    if args.watcher_type == "list":
        options = dict(
            description=args.description,
            stop_on_completion=args.stop_on_completion,
            polling_interval=args.polling_interval,
            list_tag=args.list_tag,
            list_attr=args.list_attribute,
            list_attr_val=args.list_attribute_value,
            target_tag=args.target_tag,
            target_attr=args.target_attribute,
            target_attr_val=args.target_attribute_value,
        )
        watcher = ListWatcher(args.url, options)
    elif args.watcher_type == "price":
        options = dict(
            description=args.description,
            stop_on_completion=args.stop_on_completion,
            polling_interval=args.polling_interval,
            full_xpath=args.full_xpath,
            initial_price=float(args.initial_price),
            threshold_price=args.threshold_price,
            notify_on_change=args.notify_on_change,
        )
        print(options)
        watcher = PriceWatcher(args.url, options)
    else:
        raise Exception(f"Invalid watcher_type [{args.watcher_type}]")

    configure_logger(watcher.name, args.debug)
    watcher.start()


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    try:
        main()
    except Exception as e:
        log.error(f"Exiting due to {e}")
        sys.exit()
