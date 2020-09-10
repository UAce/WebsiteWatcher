# WebsiteWatcher

WebsiteWatcher is a Python tool for running a website watcher.

## Prerequisites

Before running the WebsiteWatcher, you need to have the following prerequisites:
- Clone the repository
- Python 3 and pip installed
- Google Chrome installed
- ChromeDriver matching your Google Chrome version (see ChromeDriver versions [here](https://chromedriver.storage.googleapis.com/index.html))
_Note: the chromeDriver needs to be in the root directory of the repository_

## Installation

Run the following command to install the dependencies:

```
pip install -r requirements.txt
```

You can also run the setup script

```
python setup.py install --user
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
  --polling-interval POLLING_INTERVAL
                        Seconds to wait between each poll. Default is 60
  --notification-method {email,sms}
                        The method of notification. Default is email.
  --debug               Show debug logs
```

## List Watcher

Detects change in a list of element.

```
usage: websiteWatcher.py list [-h] --url URL --list-tag LIST_TAG
                              --list-attribute LIST_ATTRIBUTE
                              --list-attribute-value LIST_ATTRIBUTE_VALUE
                              --target-tag TARGET_TAG --target-attribute
                              TARGET_ATTRIBUTE --target-attribute-value
                              TARGET_ATTRIBUTE_VALUE
```

## Price Watcher

Detects price change of an element.
