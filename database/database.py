from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Storage directory
DATABASE_DIR = BASE_DIR / "storage"
DATABASE_DIR.mkdir(exist_ok=True)

# SQLite database file
DATABASE_PATH = DATABASE_DIR / "mindease.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Database engine
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)