import os
import logging
import argparse
from argparse import Namespace
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import IO

from websiteWatcher.settings.config import (
    config,
    email_api_key,
    email_sender,
    email_recipients,
)
from websiteWatcher.common.logger import color_formatter, default_formatter

log = logging.getLogger(__name__)


def configure_logger(watcher_name: str, debug: bool = False) -> None:
    log_level = debug if debug else config["log_level"]
    console = logging.StreamHandler()
    console.setFormatter(color_formatter)
    log_file = logging.FileHandler(filename=f"{config['log_dir']}/{watcher_name}.log")
    log_file.setFormatter(default_formatter)
    logging.basicConfig(level=log_level, handlers=[console, log_file])


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(description=config["project"]["description"])
    parser.add_argument(
        "--polling-interval",
        type=int,
        help="Seconds to wait between each poll. Default is 60",
    )
    parser.add_argument(
        "--notification-method",
        type=str,
        default="email",
        choices=["email", "sms"],
        help="The method of notification. Default is email",
    )
    parser.add_argument("--debug", action="store_true", help="Show debug logs")
    parser.add_argument("--stop-on-completion", action="store_true",
                        help="Stop the watcher when it completes. Default is disabled")

    # Create Subparsers for different types of watchers
    subparsers = parser.add_subparsers(dest="watcher_type", help="types of Watcher")
    subparsers.required = True
    # List
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument(
        "--url", type=str, help="the url of the web page to watch", required=True
    )
    list_parser.add_argument(
        "--description",
        type=str,
        help="A short description for the watcher",
        required=True,
    )
    list_parser.add_argument(
        "--list-tag", type=str, help="the HTML tag of the list to watch", required=True
    )
    list_parser.add_argument(
        "--list-attribute",
        type=str,
        help="an HTML attribute of the list element",
        required=True,
    )
    list_parser.add_argument(
        "--list-attribute-value",
        type=str,
        help="the value of the HTML attribute for the list element",
        required=True,
    )
    list_parser.add_argument(
        "--target-tag", type=str, help="the HTML tag of the target item", required=True
    )
    list_parser.add_argument(
        "--target-attribute",
        type=str,
        help="an HTML attribute of the target item",
        required=True,
    )
    list_parser.add_argument(
        "--target-attribute-value",
        type=str,
        help="the value of the HTML attribute for the target item",
        required=True,
    )

    # Price
    price_parser = subparsers.add_parser("price")
    price_parser.add_argument(
        "--url", type=str, help="the url of the web page to watch", required=True
    )
    price_parser.add_argument(
        "--description",
        type=str,
        help="A short description for the watcher",
        required=True,
    )
    price_parser.add_argument(
        "--initial-price", type=float, help="the initial price of the item", required=True
    )
    price_parser.add_argument(
        "--full-xpath", type=str, help="the full xpath of the price element", required=True
    )
    price_parser.add_argument(
        "--threshold-price", type=float, help="the threshold price after which you want to be notified", required=False
    )
    price_parser.add_argument(
        "--notify-on-change", help="whether to notify when the price changes. Default is disabled", required=False, action='store_true'
    )

    # Attempt to parse unparsed optional arguments that are out of order
    args, unparsed_args = parser.parse_known_args()
    while len(unparsed_args):
        args, unparsed_args = parser.parse_known_args(unparsed_args, args)
    return args


def send_email(subject: str = None, content: str = None) -> None:
    # For each recipient, send an email
    for recipient in email_recipients:
        message = Mail(
            from_email=email_sender,
            to_emails=recipient,
            subject=subject or "Henlo World",
            html_content=content or "test",
        )
        try:
            log.info(f"Sending email from {email_sender} to {recipient}")
            sg = SendGridAPIClient(email_api_key)
            response = sg.send(message)

            if response.status_code == 202:
                log.info("Email sent!")
            else:
                log.error("Email failed to send")
        except Exception as e:
            log.error(e)


def read_file(path_to_file: str) -> IO:
    return open(path_to_file).read()
