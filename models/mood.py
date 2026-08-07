"""
Mood model for the MindEase application.

Stores mood check-ins made by users.
"""

from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class Mood(BaseModel):
    """
    Represents a mood check-in made by a user.
    """

    __tablename__ = "moods"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    mood: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    note: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )