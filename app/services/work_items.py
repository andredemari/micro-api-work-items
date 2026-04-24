from sqlalchemy.orm import Session

from app.db.models import WorkItem
from app.repositories import work_item_repository
from app.schemas.work_items import WorkItemCreate, WorkItemUpdate


def create_work_item(db: Session, data: WorkItemCreate) -> WorkItem:
    """Persist a new work item and return the refreshed ORM record."""
    values = data.model_dump()
    values["metadata_json"] = values.pop("metadata")
    return work_item_repository.create_work_item(db, values)


def list_work_items(db: Session) -> list[WorkItem]:
    """Return all persisted work items ordered by identifier."""
    return work_item_repository.list_work_items(db)


def get_work_item(db: Session, work_item_id: int) -> WorkItem | None:
    """Return a persisted work item, or None when it does not exist."""
    return work_item_repository.get_work_item(db, work_item_id)


def update_work_item(
    db: Session,
    work_item_id: int,
    data: WorkItemUpdate,
) -> WorkItem | None:
    """Partially update a work item, returning None when it is missing."""
    values = data.model_dump(exclude_unset=True)
    if "metadata" in values:
        values["metadata_json"] = values.pop("metadata")

    return work_item_repository.update_work_item(db, work_item_id, values)


def delete_work_item(db: Session, work_item_id: int) -> bool:
    """Delete a work item, returning False when it is missing."""
    return work_item_repository.delete_work_item(db, work_item_id)
