"""
Weekly Wellness Report model.
"""

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel


class WeeklyReport(BaseModel):

    __tablename__ = "weekly_reports"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    report_content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )