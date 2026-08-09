"""
Journal model for the MindEase application.

Stores journal entries created by users.
"""

from typing import Optional

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class Journal(BaseModel):
    """
    Represents a journal entry created by a user.
    """

    __tablename__ = "journal_entries"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mood: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )