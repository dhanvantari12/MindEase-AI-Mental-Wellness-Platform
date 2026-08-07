"""
Authentication service for MindEase.
"""

from sqlalchemy import select

from database.session import get_db
from features.auth.utils import hash_password, verify_password
from features.auth.validator import (
    validate_user_email,
    validate_user_password,
)
from models.user import User


def get_user_by_email(email: str) -> User | None:
    """
    Return a user by email.
    """

    email = email.strip().lower()

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

    # Normalize input
    full_name = full_name.strip()
    email = email.strip().lower()

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

        # Check if user already exists
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


def login_user(
    email: str,
    password: str,
) -> tuple[bool, str, User | None]:
    """
    Authenticate a user.
    """

    # Normalize email
    email = email.strip().lower()

    # Find user
    user = get_user_by_email(email)

    if user is None:
        return False, "No account found with this email.", None

    # Verify password
    if not verify_password(password, user.password_hash):
        return False, "Incorrect password.", None

    return True, "Login successful!", user

"""
Mood service for MindEase.

Handles creating and retrieving mood check-ins.
"""

from sqlalchemy import select

from database.session import get_db
from models.mood import Mood


def create_mood(
    user_id: str,
    mood: str,
    note: str | None = None,
) -> Mood:
    """
    Create and save a new mood check-in.
    """

    mood_entry = Mood(
        user_id=user_id,
        mood=mood,
        note=note.strip() if note else None,
    )

    with get_db() as db:
        db.add(mood_entry)
        db.commit()
        db.refresh(mood_entry)

        return mood_entry


def get_user_moods(
    user_id: str,
) -> list[Mood]:
    """
    Return all mood check-ins for a user.

    Newest moods are returned first.
    """

    with get_db() as db:
        statement = (
            select(Mood)
            .where(Mood.user_id == user_id)
            .order_by(Mood.created_at.desc())
        )

        return list(db.scalars(statement).all())


def get_latest_mood(
    user_id: str,
) -> Mood | None:
    """
    Return the user's most recent mood.
    """

    with get_db() as db:
        statement = (
            select(Mood)
            .where(Mood.user_id == user_id)
            .order_by(Mood.created_at.desc())
            .limit(1)
        )

        return db.scalar(statement)