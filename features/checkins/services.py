from datetime import date

from sqlalchemy import select

from database.session import get_db
from models.daily_checkin import DailyCheckIn


def create_checkin(
    user_id: str,
    checkin_type: str,
    content: str,
) -> DailyCheckIn:

    checkin = DailyCheckIn(
        user_id=user_id,
        checkin_type=checkin_type,
        content=content,
        checkin_date=date.today(),
    )

    with get_db() as db:

        db.add(checkin)

        db.commit()

        db.refresh(checkin)

        return checkin


def get_today_checkins(
    user_id: str,
) -> list[DailyCheckIn]:

    with get_db() as db:

        statement = (
            select(DailyCheckIn)
            .where(
                DailyCheckIn.user_id == user_id,
                DailyCheckIn.checkin_date == date.today(),
            )
        )

        return list(
            db.scalars(statement).all()
        )