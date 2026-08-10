"""
Persistent authentication session service for MindEase.

Handles:
- Creating persistent login sessions
- Validating session tokens
- Finding users from sessions
- Deleting sessions during logout
"""

import hashlib
import secrets
from datetime import datetime, timedelta

from sqlalchemy import select

from database.session import get_db
from models.login_session import LoginSession
from models.user import User


# ---------------------------------------------------------
# Session Configuration
# ---------------------------------------------------------

SESSION_DURATION_DAYS = 7


# ---------------------------------------------------------
# Token Helpers
# ---------------------------------------------------------

def generate_session_token() -> str:
    """
    Generate a cryptographically secure session token.
    """

    return secrets.token_urlsafe(32)


def hash_session_token(token: str) -> str:
    """
    Hash a session token before storing it in the database.
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


# ---------------------------------------------------------
# Create Session
# ---------------------------------------------------------

def create_session(
    user_id: str,
) -> str:
    """
    Create a persistent login session.

    Returns:
        The raw session token that should be
        stored in the browser cookie.
    """

    raw_token = generate_session_token()

    token_hash = hash_session_token(
        raw_token
    )

    expires_at = (
        datetime.utcnow()
        + timedelta(days=SESSION_DURATION_DAYS)
    )

    session = LoginSession(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    with get_db() as db:

        db.add(session)

        db.commit()

    return raw_token


# ---------------------------------------------------------
# Get User From Session
# ---------------------------------------------------------

def get_user_from_session(
    token: str,
) -> User | None:
    """
    Validate a session token and return
    the associated user.

    Returns None if the token is invalid
    or the session has expired.
    """

    if not token:
        return None

    token_hash = hash_session_token(
        token
    )

    with get_db() as db:

        statement = (
            select(LoginSession)
            .where(
                LoginSession.token_hash
                == token_hash
            )
        )

        session = db.scalar(statement)

        if session is None:
            return None

        # -------------------------------------------------
        # Check expiration
        # -------------------------------------------------

        if session.expires_at < datetime.utcnow():

            db.delete(session)
            db.commit()

            return None

        # -------------------------------------------------
        # Get associated user
        # -------------------------------------------------

        user = db.get(
            User,
            session.user_id,
        )

        return user


# ---------------------------------------------------------
# Delete Session
# ---------------------------------------------------------

def delete_session(
    token: str,
) -> None:
    """
    Delete a persistent login session.
    """

    if not token:
        return

    token_hash = hash_session_token(
        token
    )

    with get_db() as db:

        statement = (
            select(LoginSession)
            .where(
                LoginSession.token_hash
                == token_hash
            )
        )

        session = db.scalar(statement)

        if session:

            db.delete(session)

            db.commit()