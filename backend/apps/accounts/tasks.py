from celery import shared_task
from djresttoolkit.mail import EmailSender

from apps.accounts.models import User


@shared_task
def send_signup_email(user_id: int, activate_url: str) -> None:
    """Creating the Email Service and send it to user."""
    user = User.objects.get(pk=user_id)

    email_sender = EmailSender(
        {
            "subject": "Verify Your Account",
            "from_email": None,
            "context": {"user": user, "activate_url": activate_url},
            "template": {
                "text": "accounts/account_verification/confirm_message.txt",
                "html": "accounts/account_verification/confirm_message.html",
            },
        }
    )

    # Send account verification email
    email_sender.send(to=[user.email])
