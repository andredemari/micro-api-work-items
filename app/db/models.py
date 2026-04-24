from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for persisted records."""
    return datetime.now(timezone.utc)


class WorkItem(Base):
    """SQLAlchemy persistence model for a generic work item."""

    __tablename__ = "work_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    type: Mapped[str] = mapped_column(String(30), nullable=False, default="task")
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
