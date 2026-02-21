"""
Notification service for sending emails (e.g. verification link).
"""
import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_verification_email(email: str, verification_token: str) -> None:
    """
    Send verification email with link containing the token.

    Args:
        email: Recipient email
        verification_token: Encrypted token (user id) for the verification link
    """
    base_url = getattr(
        settings,
        'SITE_URL',
        'http://localhost:8000',
    ).rstrip('/')
    verify_url = f"{base_url}/api/auth/verify-email/?token={verification_token}"

    use_mock = getattr(settings, 'EMAIL_VERIFICATION_MOCK', True)
    if use_mock:
        logger.info(
            "Verification email (mock) for %s: %s",
            email,
            verify_url,
        )
        return

    subject = "Verify your email - Matcha"
    message = f"Click to verify your email: {verify_url}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@matcha.local')
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=False,
    )
