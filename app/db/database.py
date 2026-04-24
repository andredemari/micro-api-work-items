import os
from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/work_items.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}


def ensure_sqlite_parent_directory(database_url: str) -> None:
    """Create the parent directory for file-based SQLite databases."""
    url = make_url(database_url)
    if url.get_backend_name() != "sqlite" or not url.database:
        return

    if url.database == ":memory:":
        return

    Path(url.database).parent.mkdir(parents=True, exist_ok=True)


ensure_sqlite_parent_directory(DATABASE_URL)

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


def init_db() -> None:
    """Create database tables for the local SQLite-backed MVP."""
    from app.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and close it after the request finishes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
