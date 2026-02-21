"""
Token service for verification links.
Encrypts/decrypts user id to a URL-safe token (reversible).
"""
import hashlib
import logging
from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet
from django.conf import settings

from exceptions import InvalidVerificationToken

logger = logging.getLogger(__name__)


def _get_fernet() -> Fernet:
    """Build Fernet instance from Django SECRET_KEY (32 bytes derived, base64url)."""
    key = urlsafe_b64encode(
        hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    ).decode()
    return Fernet(key.encode())


def encrypt(user_id: int) -> str:
    """
    Encrypt user_id to a URL-safe token.

    Args:
        user_id: User ID to encode

    Returns:
        URL-safe string token
    """
    fernet = _get_fernet()
    payload = str(user_id).encode()
    return fernet.encrypt(payload).decode()


def decrypt(token: str) -> int:
    """
    Decrypt token to user_id.

    Args:
        token: Token from verification link

    Returns:
        User ID

    Raises:
        InvalidVerificationToken: If token is invalid or corrupt
    """
    if not token or not token.strip():
        raise InvalidVerificationToken("Token is empty")
    try:
        fernet = _get_fernet()
        payload = fernet.decrypt(token.encode()).decode()
        return int(payload)
    except Exception as e:
        logger.warning("Failed to decrypt verification token: %s", e)
        raise InvalidVerificationToken("Invalid or corrupt verification token") from e
