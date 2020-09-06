import logging
import argparse
from argparse import Namespace, ArgumentParser
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import config, email_api_key, email_sender, email_recipient
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


def validate_args_dependencies(parser: ArgumentParser, watcher_type: str,
                               args: Namespace) -> None:
    # Validate args dependencies
    if watcher_type == 'list':
        if (not args.list_tag or not args.list_attribute
                or not args.list_attribute_value or not args.target_tag
                or not args.target_attribute
                or not args.target_attribute_value):
            parser.error(
                "'list' watcher_type requires list-tag, list-attribute, "
                "list-attribute-value, target-tag, target-attribute, "
                "target-attribute-value")
    elif watcher_type == 'price':
        # TODO: TBD
        pass
    else:
        raise Exception(f'Invalid watcher_type [{watcher_type}]')


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser(
        description=config['project']['description'])
    parser.add_argument(
        'watcher_type',
        type=str,
        choices=['list', 'price'],
        help='the watcher type')
    parser.add_argument(
        '--url',
        type=str,
        help='the url of the web page to watch',
        required=True)
    parser.add_argument(
        '--list-tag', type=str, help='the HTML tag of the list to watch')
    parser.add_argument(
        '--list-attribute',
        type=str,
        help='an HTML attribute of the list element')
    parser.add_argument(
        '--list-attribute-value',
        type=str,
        help='the value of the HTML attribute for the list element')
    parser.add_argument(
        '--target-tag', type=str, help='the HTML tag of the target item')
    parser.add_argument(
        '--target-attribute',
        type=str,
        help='an HTML attribute of the target item')
    parser.add_argument(
        '--target-attribute-value',
        type=str,
        help='the value of the HTML attribute for the target item')
    parser.add_argument(
        '--initial-count',
        type=int,
        help='Initial number of items in the list')
    parser.add_argument(
        '--polling-interval',
        type=int,
        default=60,
        help='Number of seconds to wait between each poll')
    args = parser.parse_args()
    validate_args_dependencies(parser, args.watcher_type, args)
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
        # log.debug(response.status_code)
        # log.debug(response.body)
        # log.debug(response.headers)
    except Exception as e:
        log.error(e)
