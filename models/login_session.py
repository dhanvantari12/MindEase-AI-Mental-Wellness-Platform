"""
Login session model for MindEase.

Stores persistent browser login sessions.
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class LoginSession(BaseModel):
    """
    Persistent login session associated with a user.
    """

    __tablename__ = "login_sessions"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    token_hash: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
        index=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )