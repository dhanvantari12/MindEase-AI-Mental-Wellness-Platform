"""
Conversation model for MindEase.
"""

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class Conversation(BaseModel):
    """
    Stores a Safe Space conversation message.
    """

    __tablename__ = "conversations"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )