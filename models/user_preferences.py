"""
User preferences model for MindEase.

Stores personal application preferences for each user.
"""

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class UserPreferences(BaseModel):
    """
    Represents application preferences for a user.
    """

    __tablename__ = "user_preferences"

    # ---------------------------------------------------------
    # User
    # ---------------------------------------------------------

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Reminder Preferences
    # ---------------------------------------------------------

    reminders_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ---------------------------------------------------------
    # Wellness Preferences
    # ---------------------------------------------------------

    daily_checkin_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    journal_prompts_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )