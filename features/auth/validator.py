"""
Validation functions for authentication.
"""

import re

from email_validator import EmailNotValidError, validate_email


def validate_user_email(email: str) -> tuple[bool, str]:
    """
    Validate email format.
    """
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as error:
        return False, str(error)


def validate_user_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    """

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."

    return True, ""