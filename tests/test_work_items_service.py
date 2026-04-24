from sqlalchemy.orm import Session

from app.schemas.work_items import WorkItemCreate, WorkItemUpdate
from app.services import work_items as work_item_service


def test_service_create_list_get_update_and_delete_work_item(
    db_session: Session,
) -> None:
    created = work_item_service.create_work_item(
        db_session,
        WorkItemCreate(
            title="Prepare release checklist",
            description="Create a short checklist for the next release.",
            status="open",
            priority="medium",
            type="task",
            source="manual",
            tags=["release", "checklist"],
            metadata={"estimate": 2, "reviewed": False},
        ),
    )

    assert created.id == 1
    assert created.tags == ["release", "checklist"]
    assert created.metadata_json == {"estimate": 2, "reviewed": False}

    assert work_item_service.list_work_items(db_session) == [created]
    assert work_item_service.get_work_item(db_session, created.id) == created

    original_created_at = created.created_at
    original_updated_at = created.updated_at

    updated = work_item_service.update_work_item(
        db_session,
        created.id,
        WorkItemUpdate(
            status="in_progress",
            priority="high",
            metadata={"estimate": 3, "reviewed": True},
        ),
    )

    assert updated is not None
    assert updated.status == "in_progress"
    assert updated.priority == "high"
    assert updated.tags == ["release", "checklist"]
    assert updated.metadata_json == {"estimate": 3, "reviewed": True}
    assert updated.created_at == original_created_at
    assert updated.updated_at is not None
    assert updated.updated_at >= original_updated_at

    assert work_item_service.delete_work_item(db_session, created.id) is True
    assert work_item_service.get_work_item(db_session, created.id) is None
    assert work_item_service.list_work_items(db_session) == []


def test_service_missing_work_item_returns_none_or_false(db_session: Session) -> None:
    assert work_item_service.get_work_item(db_session, 999) is None
    assert (
        work_item_service.update_work_item(
            db_session,
            999,
            WorkItemUpdate(status="done"),
        )
        is None
    )
    assert work_item_service.delete_work_item(db_session, 999) is False
