from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import WorkItem, utc_now
from app.schemas.work_items import WorkItemCreate, WorkItemUpdate


def create_work_item(db: Session, data: WorkItemCreate) -> WorkItem:
    """Persist a new work item and return the refreshed ORM record."""
    values = data.model_dump()
    values["metadata_json"] = values.pop("metadata")
    work_item = WorkItem(**values)

    db.add(work_item)
    db.commit()
    db.refresh(work_item)
    return work_item


def list_work_items(db: Session) -> list[WorkItem]:
    """Return all persisted work items ordered by identifier."""
    statement = select(WorkItem).order_by(WorkItem.id)
    return list(db.scalars(statement).all())


def get_work_item(db: Session, work_item_id: int) -> WorkItem | None:
    """Return a persisted work item, or None when it does not exist."""
    return db.get(WorkItem, work_item_id)


def update_work_item(
    db: Session,
    work_item_id: int,
    data: WorkItemUpdate,
) -> WorkItem | None:
    """Partially update a work item, returning None when it is missing."""
    work_item = get_work_item(db, work_item_id)
    if work_item is None:
        return None

    values = data.model_dump(exclude_unset=True)
    if "metadata" in values:
        values["metadata_json"] = values.pop("metadata")

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
