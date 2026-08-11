"""
Reminder model for MindEase.

Stores personal reminders created by users.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class Reminder(BaseModel):
    """
    Represents a reminder created by a user.
    """

    __tablename__ = "reminders"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    reminder_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )