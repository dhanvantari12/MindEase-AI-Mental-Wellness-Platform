from datetime import date, timedelta

from sqlalchemy import select

from database.session import get_db
from models.daily_checkin import DailyCheckIn


def get_current_streak(
    user_id: str,
) -> int:

    with get_db() as db:

        statement = (
            select(DailyCheckIn)
            .where(
                DailyCheckIn.user_id == user_id
            )
            .order_by(
                DailyCheckIn.checkin_date.desc()
            )
        )

        checkins = list(
            db.scalars(statement).all()
        )

    if not checkins:
        return 0

    dates = {
        c.checkin_date
        for c in checkins
    }

    streak = 0
    current_day = date.today()

    while current_day in dates:

        streak += 1
        current_day -= timedelta(days=1)

    return streak


def get_longest_streak(
    user_id: str,
) -> int:

    with get_db() as db:

        statement = (
            select(DailyCheckIn)
            .where(
                DailyCheckIn.user_id == user_id
            )
            .order_by(
                DailyCheckIn.checkin_date.asc()
            )
        )

        checkins = list(
            db.scalars(statement).all()
        )

    if not checkins:
        return 0

    dates = sorted(
        {
            c.checkin_date
            for c in checkins
        }
    )

    longest = 1
    current = 1

    for i in range(1, len(dates)):

        if (
            dates[i]
            ==
            dates[i - 1]
            + timedelta(days=1)
        ):
            current += 1
            longest = max(
                longest,
                current,
            )

        else:
            current = 1

    return longest