"""
Creates all database tables for the MindEase application.

Run this file when setting up the project or adding new database models.
"""

from database.database import engine
from models.base import Base

# Import all models so SQLAlchemy registers them

from models.user import User  # noqa: F401
from models.conversation import Conversation  # noqa: F401
from models.mood import Mood  # noqa: F401
from models.journal import Journal  # noqa: F401
from models.login_session import LoginSession  # noqa: F401
from models.reminder import Reminder  # noqa: F401
from models.user_preferences import UserPreferences  # noqa: F401
from models.ai_memory import AIMemory  # noqa: F401
from models.weekly_report import WeeklyReport
from models.daily_checkin import DailyCheckIn


def create_database() -> None:
    """
    Create all tables defined in SQLAlchemy models.
    """

    Base.metadata.create_all(bind=engine)

    print("✅ Database tables checked/created successfully!")


if __name__ == "__main__":
    create_database()