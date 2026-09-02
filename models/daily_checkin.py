from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import BaseModel

from datetime import date
from sqlalchemy import Date


class DailyCheckIn(BaseModel):

    __tablename__ = "daily_checkins"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    checkin_date: Mapped[date] = mapped_column(
    Date,
    nullable=False,
    index=True,
    )

    morning_mood: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    night_reflection: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )