from celery import shared_task
from djresttoolkit.mail import EmailSender


@shared_task
def send_account_activation_email(email: str, uri: str) -> None:
    """Creating the Email Service and send it to user."""
    email_sender = EmailSender(
        {
            "subject": "Verify Your Account",
            "from_email": None,
            "context": {
                "site_name": "Drts-Init",
                "email": email,
                "uri": uri,
            },
            "template": {
                "text": "accounts/activation/message.txt",
                "html": "accounts/activation/message.html",
            },
        }
    )

    # Send account activation email
    email_sender.send(to=[email])


@shared_task
def send_account_deactivation_email(email: str) -> None:
    """Creating the Email Service and send it to user."""
    email_sender = EmailSender(
        {
            "subject": "Verify Your Account",
            "from_email": None,
            "context": {"site_name": "Drts-Init", "email": email},
            "template": {
                "text": "accounts/deactivation/message.txt",
                "html": "accounts/deactivation/message.html",
            },
        }
    )

    # Send account verification email
    email_sender.send(to=[email])


@shared_task
def send_password_change_email(email: str) -> None:
    """Creating the Email Service and send it to user."""
    email_sender = EmailSender(
        {
            "subject": "Verify Your Account",
            "from_email": None,
            "context": {
                "site_name": "Drts-Init",
                "email": email,
            },
            "template": {
                "text": "accounts/password/change/message.txt",
                "html": "accounts/password/change/message.html",
            },
        }
    )

    # Send account verification email
    email_sender.send(to=[email])


@shared_task
def send_password_reset_email(email: str, uri: str) -> None:
    """Creating the Email Service and send it to user."""
    email_sender = EmailSender(
        {
            "subject": "Verify Your Account",
            "from_email": None,
            "context": {
                "site_name": "Drts-Init",
                "email": email,
                "uri": uri,
            },
            "template": {
                "text": "accounts/password/reset/message.txt",
                "html": "accounts/password/reset/message.html",
            },
        }
    )

    # Send account verification email
    email_sender.send(to=[email])
