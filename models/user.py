"""
User model for the MindEase application.

Stores authentication and profile information for each registered user.
"""

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a registered user.
    """

    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    profile_image: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )