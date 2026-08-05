"""
Database session helper.
"""

from contextlib import contextmanager

from database.database import SessionLocal


@contextmanager
def get_db():
    """
    Yield a database session and close it automatically.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()