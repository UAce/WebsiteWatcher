# WebsiteWatcher

WebsiteWatcher is a Python tool for running a website watcher.

## Installation

...

## Usage

Look at the [sample commands](https://github.com/UAce/WebsiteWatcher/tree/master/example) for examples.

```bash
usage: main.py [-h] --url URL [--list-tag LIST_TAG]
               [--list-attribute LIST_ATTRIBUTE]
               [--list-attribute-value LIST_ATTRIBUTE_VALUE]
               [--target-tag TARGET_TAG] [--target-attribute TARGET_ATTRIBUTE]
               [--target-attribute-value TARGET_ATTRIBUTE_VALUE]
               [--initial-count INITIAL_COUNT]
               [--polling-interval POLLING_INTERVAL]
               {list,price}

WebsiteWatcher is a Python CLI tool for running a website watcher

positional arguments:
  {list,price}          the watcher type

optional arguments:
  -h, --help            show this help message and exit
  --url URL             the url of the web page to watch
  --list-tag LIST_TAG   the HTML tag of the list to watch
  --list-attribute LIST_ATTRIBUTE
                        an HTML attribute of the list element
  --list-attribute-value LIST_ATTRIBUTE_VALUE
                        the value of the HTML attribute for the list element
  --target-tag TARGET_TAG
                        the HTML tag of the target item
  --target-attribute TARGET_ATTRIBUTE
                        an HTML attribute of the target item
  --target-attribute-value TARGET_ATTRIBUTE_VALUE
                        the value of the HTML attribute for the target item
  --initial-count INITIAL_COUNT
                        Initial number of items in the list
  --polling-interval POLLING_INTERVAL
                        Number of seconds to wait between each poll

```

## List Watcher

Detects change in a list of element.

## Price Watcher

Detects price change of an element.
