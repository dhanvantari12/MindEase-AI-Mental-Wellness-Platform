"""
Reminder and Daily Check-In services.

Handles:
- Morning mood check-ins
- Night reflections
- Daily streaks
"""

from datetime import date, timedelta

from sqlalchemy import select

from database.session import get_db
from models.daily_checkin import DailyCheckIn


# ---------------------------------------------------------
# Get Today's Check-In
# ---------------------------------------------------------

def get_today_checkin(
    user_id: str,
) -> DailyCheckIn | None:

    today = date.today()

    with get_db() as db:

        statement = (
            select(DailyCheckIn)
            .where(
                DailyCheckIn.user_id == user_id,
                DailyCheckIn.checkin_date == today,
            )
        )

        return db.scalar(statement)


# ---------------------------------------------------------
# Save Morning Mood
# ---------------------------------------------------------

def save_morning_checkin(
    user_id: str,
    mood: str,
) -> DailyCheckIn:

    today = date.today()

    with get_db() as db:

        statement = (
            select(DailyCheckIn)
            .where(
                DailyCheckIn.user_id == user_id,
                DailyCheckIn.checkin_date == today,
            )
        )

        checkin = db.scalar(statement)

        if checkin is None:

            checkin = DailyCheckIn(
                user_id=user_id,
                checkin_date=today,
                morning_mood=mood,
            )

            db.add(checkin)

        else:

            checkin.morning_mood = mood

        db.commit()
        db.refresh(checkin)

        return checkin


# ---------------------------------------------------------
# Save Night Reflection
# ---------------------------------------------------------

def save_night_reflection(
    user_id: str,
    reflection: str,
) -> DailyCheckIn:

    today = date.today()

    with get_db() as db:

        statement = (
            select(DailyCheckIn)
            .where(
                DailyCheckIn.user_id == user_id,
                DailyCheckIn.checkin_date == today,
            )
        )

        checkin = db.scalar(statement)

        if checkin is None:

            checkin = DailyCheckIn(
                user_id=user_id,
                checkin_date=today,
                night_reflection=reflection,
            )

            db.add(checkin)

        else:

            checkin.night_reflection = reflection

        db.commit()
        db.refresh(checkin)

        return checkin


# ---------------------------------------------------------
# Calculate Daily Streak
# ---------------------------------------------------------

def calculate_streak(
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