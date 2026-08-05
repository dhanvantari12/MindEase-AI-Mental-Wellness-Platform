"""
Creates all database tables for the MindEase application.
Run this file once when setting up the project.
"""

from database.database import engine
from models.base import Base

# Import all models here
from models.user import User  # noqa: F401


def create_database() -> None:
    """
    Create all tables defined in SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database created successfully!")


if __name__ == "__main__":
    create_database()