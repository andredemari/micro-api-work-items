from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.work_item_model import WorkItem, utc_now
from app.schemas.work_items import WorkItemPriority, WorkItemStatus


def create_work_item(db: Session, values: Mapping[str, Any]) -> WorkItem:
    """Persist a new work item and return the refreshed ORM record."""
    work_item = WorkItem(**values)

    db.add(work_item)
    db.commit()
    db.refresh(work_item)
    return work_item


def list_work_items(
    db: Session,
    status: WorkItemStatus | None = None,
    priority: WorkItemPriority | None = None,
) -> list[WorkItem]:
    """Return matching work items ordered by identifier."""
    statement = select(WorkItem).order_by(WorkItem.id)
    if status is not None:
        statement = statement.where(WorkItem.status == status)
    if priority is not None:
        statement = statement.where(WorkItem.priority == priority)
    return list(db.scalars(statement).all())


def get_work_item(db: Session, work_item_id: int) -> WorkItem | None:
    """Return a persisted work item, or None when it does not exist."""
    return db.get(WorkItem, work_item_id)


def update_work_item(
    db: Session,
    work_item_id: int,
    values: Mapping[str, Any],
) -> WorkItem | None:
    """Update persisted fields, returning None when the item is missing."""
    work_item = get_work_item(db, work_item_id)
    if work_item is None:
        return None

    for field_name, value in values.items():
        setattr(work_item, field_name, value)

    work_item.updated_at = utc_now()
    db.commit()
    db.refresh(work_item)
    return work_item


def delete_work_item(db: Session, work_item_id: int) -> bool:
    """Delete a work item, returning False when it is missing."""
    work_item = get_work_item(db, work_item_id)
    if work_item is None:
        return False

    db.delete(work_item)
    db.commit()
    return True
