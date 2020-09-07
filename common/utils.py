import logging
import argparse
from argparse import Namespace
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from settings.config import (config, email_api_key, email_sender,
                             email_recipient)
from common.logger import color_formatter, default_formatter

log = logging.getLogger(__name__)


def configure_logger(watcher_name: str) -> None:
    console = logging.StreamHandler()
    console.setFormatter(color_formatter)
    log_file = logging.FileHandler(
        filename=f"{config['log_dir']}/{watcher_name}.log")
    log_file.setFormatter(default_formatter)
    logging.basicConfig(
        level=config['log_level'], handlers=[console, log_file])


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(
        description=config['project']['description'])
    parser.add_argument(
        '--polling-interval',
        type=int,
        default=60,
        help='Number of seconds to wait between each poll')
    parser.add_argument(
        '--notification-method',
        type=str,
        default='email',
        choices=['email', 'sms'],
        help='The method of notification')

    # Create Subparsers for different types of watchers
    subparsers = parser.add_subparsers(
        dest='watcher_type', help='types of Watcher')

    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument(
        '--url',
        type=str,
        help='the url of the web page to watch',
        required=True)
    list_parser.add_argument(
        '--list-tag',
        type=str,
        help='the HTML tag of the list to watch',
        required=True)
    list_parser.add_argument(
        '--list-attribute',
        type=str,
        help='an HTML attribute of the list element',
        required=True)
    list_parser.add_argument(
        '--list-attribute-value',
        type=str,
        help='the value of the HTML attribute for the list element',
        required=True)
    list_parser.add_argument(
        '--target-tag',
        type=str,
        help='the HTML tag of the target item',
        required=True)
    list_parser.add_argument(
        '--target-attribute',
        type=str,
        help='an HTML attribute of the target item',
        required=True)
    list_parser.add_argument(
        '--target-attribute-value',
        type=str,
        help='the value of the HTML attribute for the target item',
        required=True)

    # Price
    price_parser = subparsers.add_parser("price")
    price_parser.add_argument(
        '--url',
        type=str,
        help='the url of the web page to watch',
        required=True)
    price_parser.add_argument(
        '--price', type=float, help='initial price of the item', required=True)

    # Attempt to parse unparsed optional arguments that are out of order
    args, unparsed_args = parser.parse_known_args()
    while len(unparsed_args):
        args, unparsed_args = parser.parse_known_args(unparsed_args, args)
    return args


def send_email(subject: str = None, content: str = None) -> None:
    message = Mail(
        from_email=email_sender,
        to_emails=email_recipient,
        subject=subject or 'Henlo World',
        html_content=content or 'test')
    try:
        sg = SendGridAPIClient(email_api_key)
        sg.send(message)
    except Exception as e:
        log.error(e)
