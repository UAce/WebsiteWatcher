# WebsiteWatcher

WebsiteWatcher is a Python Command line tool that watches a website and notifies the user via email or sms.

## Prerequisites

Before running the WebsiteWatcher, you need to have the following prerequisites:

- Python 3
- Pip
- Google Chrome / Chromium
- ChromeDriver matching your Google Chrome/CHromium version (see ChromeDriver versions [here](https://chromedriver.storage.googleapis.com/index.html))

_Note: the chromeDriver needs to be in the root directory of the repository_

## Installation

Clone the repository and run the following command to install the dependencies:

```
pip install -r requirements.txt
```

## Usage

Look at the [sample commands](https://github.com/UAce/WebsiteWatcher/tree/master/example) for examples.

```bash
usage: websiteWatcher.py [-h] [--polling-interval POLLING_INTERVAL]
                         [--notification-method {email,sms}] [--debug]
                         {list,price} ...

WebsiteWatcher is a Python CLI tool for running a website watcher

positional arguments:
  {list,price}          types of Watcher

optional arguments:
  -h, --help            show this help message and exit
  --description DESCRIPTION
                        A short description for the watcher
  --polling-interval POLLING_INTERVAL
                        Seconds to wait between each poll. Default is 60
  --notification-method {email,sms}
                        The method of notification. Default is email
  --debug               Show debug logs
  --stop-on-completion  Stop the watcher when it completes. Default is disabled
```

## List Watcher

Detects change in a list of element.

```
usage: websiteWatcher.py list [-h]  --url URL
                                    --list-tag LIST_TAG
                                    --list-attribute LIST_ATTRIBUTE
                                    --list-attribute-value LIST_ATTRIBUTE_VALUE
                                    --target-tag TARGET_TAG
                                    --target-attribute TARGET_ATTRIBUTE
                                    --target-attribute-value TARGET_ATTRIBUTE_VALUE

options:
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
```

## Price Watcher

```
usage: websiteWatcher.py price [-h] --url URL
                                    --initial-price INITIAL_PRICE
                                    --full-xpath FULL_XPATH
                                    [--threshold-price THRESHOLD_PRICE]
                                    [--notify-on-change]

options:
  -h, --help            show this help message and exit
  --url URL             the url of the web page to watch
  --initial-price INITIAL_PRICE
                        the initial price of the item
  --full-xpath FULL_XPATH
                        the full xpath of the price element
  --threshold-price THRESHOLD_PRICE
                        the threshold price after which you want to be notified
  --notify-on-change    whether to notify when the price changes. Default is disabled
```
