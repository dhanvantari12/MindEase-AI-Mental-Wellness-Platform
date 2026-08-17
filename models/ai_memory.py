"""
AI memory model for MindEase.

Stores important long-term context that can help
personalize the AI wellness companion.
"""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class AIMemory(BaseModel):
    """
    Represents a long-term memory associated with a user.
    """

    __tablename__ = "ai_memories"

    # ---------------------------------------------------------
    # User
    # ---------------------------------------------------------

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # ---------------------------------------------------------
    # Memory Category
    # ---------------------------------------------------------

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="general",
    )

    # ---------------------------------------------------------
    # Memory Content
    # ---------------------------------------------------------

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )