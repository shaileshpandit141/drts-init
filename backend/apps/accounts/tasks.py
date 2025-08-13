from accounts.models import User
from celery import shared_task
from rest_core.email_service import Emails, EmailService, Templates


@shared_task
def send_signup_email(user_id: int, activate_url: str) -> None:
    """Creating the Email Service and send it to user."""
    user = User.objects.get(pk=user_id)

    email = EmailService(
        subject="Verify Your Account",
        emails=Emails(
            from_email=None,
            to_emails=[user.email],
        ),
        context={"user": user, "activate_url": activate_url},
        templates=Templates(
            text_template="accounts/account_verification/confirm_message.txt",
            html_template="accounts/account_verification/confirm_message.html",
        ),
    )

    # Send account verification email
    email.send(fallback=False)
