from websiteWatcher.watchers.list_watcher import ListWatcher
from websiteWatcher.common.utils import configure_logger, parse_arguments


def main() -> None:
    args = parse_arguments()
    watcher = None
    if args.watcher_type == "list":
        options = dict(
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
        # TODO: create PriceWatcher
        pass
    else:
        raise Exception(f"Invalid watcher_type [{args.watcher_type}]")

    configure_logger(watcher.name, args.debug)
    watcher.start()


if __name__ == "__main__":
    main()
