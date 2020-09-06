from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config import config, email_api_key, email_sender, email_recipient


def send_email(subject: str = None, content: str = None) -> None:
    message = Mail(
        from_email=email_sender,
        to_emails=email_recipient,
        subject=subject or 'Henlo World',
        html_content=content or 'test')
    try:
        sg = SendGridAPIClient(email_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
