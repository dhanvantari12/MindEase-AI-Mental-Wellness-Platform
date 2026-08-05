"""
Authentication service for MindEase.
"""

from sqlalchemy import select

from database.session import get_db
from features.auth.utils import hash_password
from features.auth.validator import (
    validate_user_email,
    validate_user_password,
)
from models.user import User


def get_user_by_email(email: str) -> User | None:
    """
    Return a user by email.
    """
    with get_db() as db:
        statement = select(User).where(User.email == email)
        return db.scalar(statement)


def register_user(
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
) -> tuple[bool, str]:
    """
    Register a new user.
    """

    # Validate email
    valid_email, email_message = validate_user_email(email)
    if not valid_email:
        return False, email_message

    # Validate password
    valid_password, password_message = validate_user_password(password)
    if not valid_password:
        return False, password_message

    # Confirm password
    if password != confirm_password:
        return False, "Passwords do not match."

    with get_db() as db:

        # Check existing user
        existing_user = db.scalar(
            select(User).where(User.email == email)
        )

        if existing_user:
            return False, "An account with this email already exists."

        # Create new user
        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
        )

        db.add(user)
        db.commit()

        return True, "Account created successfully!"

from features.auth.utils import verify_password


def login_user(
    email: str,
    password: str,
) -> tuple[bool, str, User | None]:
    """
    Authenticate a user.
    """

    user = get_user_by_email(email)

    if user is None:
        return False, "No account found with this email.", None

    if not verify_password(password, user.password_hash):
        return False, "Incorrect password.", None

    return True, "Login successful!", user