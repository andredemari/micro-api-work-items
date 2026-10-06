from typing import Any

import pytest
from sqlalchemy.orm import Session

from app.schemas.work_items import (
    WorkItemCreate,
    WorkItemPriority,
    WorkItemStatus,
    WorkItemUpdate,
)
from app.services import work_items as work_item_service


def _work_item_create(**overrides: Any) -> WorkItemCreate:
    payload: dict[str, Any] = {
        "title": "Prepare release checklist",
        "description": "Create a short checklist for the next release.",
        "status": "open",
        "priority": "medium",
        "type": "task",
        "source": "manual",
        "tags": ["release", "checklist"],
        "metadata": {"estimate": 2, "reviewed": False},
    }
    payload.update(overrides)
    return WorkItemCreate(**payload)


def _create_work_item(db_session: Session, **overrides: Any):
    return work_item_service.create_work_item(
        db_session,
        _work_item_create(**overrides),
    )


def test_service_list_starts_empty(db_session: Session) -> None:
    assert work_item_service.list_work_items(db_session) == []


def test_service_create_work_item_persists_fields(db_session: Session) -> None:
    created = _create_work_item(db_session)

    assert created.id == 1
    assert created.title == "Prepare release checklist"
    assert created.description == "Create a short checklist for the next release."
    assert created.status == "open"
    assert created.priority == "medium"
    assert created.type == "task"
    assert created.source == "manual"
    assert created.tags == ["release", "checklist"]
    assert created.metadata_json == {"estimate": 2, "reviewed": False}
    assert created.created_at is not None
    assert created.updated_at is not None


def test_service_list_returns_multiple_items(db_session: Session) -> None:
    first = _create_work_item(db_session, title="First work item")
    second = _create_work_item(db_session, title="Second work item")

    assert work_item_service.list_work_items(db_session) == [first, second]


@pytest.mark.parametrize(
    ("status", "priority", "expected_titles"),
    [
        (None, None, ["A", "B", "C", "D"]),
        (WorkItemStatus.OPEN, None, ["A", "B"]),
        (None, WorkItemPriority.HIGH, ["A", "C"]),
        (WorkItemStatus.OPEN, WorkItemPriority.HIGH, ["A"]),
        (WorkItemStatus.ARCHIVED, WorkItemPriority.CRITICAL, []),
    ],
)
def test_service_list_filters(
    db_session: Session,
    status: WorkItemStatus | None,
    priority: WorkItemPriority | None,
    expected_titles: list[str],
) -> None:
    items = [
        _create_work_item(db_session, title="A", status="open", priority="high"),
        _create_work_item(db_session, title="B", status="open", priority="low"),
        _create_work_item(db_session, title="C", status="done", priority="high"),
        _create_work_item(
            db_session, title="D", status="in_progress", priority="critical"
        ),
    ]

    listed = work_item_service.list_work_items(
        db_session, status=status, priority=priority
    )

    assert listed == [item for item in items if item.title in expected_titles]
    assert [item.title for item in listed] == expected_titles


@pytest.mark.parametrize("status", list(WorkItemStatus))
def test_service_list_filters_accept_each_status(
    db_session: Session, status: WorkItemStatus
) -> None:
    items = [
        _create_work_item(db_session, title=value.value, status=value)
        for value in WorkItemStatus
    ]

    assert work_item_service.list_work_items(db_session, status=status) == [
        item for item in items if item.status == status
    ]


@pytest.mark.parametrize("priority", list(WorkItemPriority))
def test_service_list_filters_accept_each_priority(
    db_session: Session, priority: WorkItemPriority
) -> None:
    items = [
        _create_work_item(db_session, title=value.value, priority=value)
        for value in WorkItemPriority
    ]

    assert work_item_service.list_work_items(db_session, priority=priority) == [
        item for item in items if item.priority == priority
    ]


@pytest.mark.parametrize(
    ("status", "priority"),
    [
        (WorkItemStatus.OPEN, None),
        (None, WorkItemPriority.HIGH),
        (WorkItemStatus.OPEN, WorkItemPriority.HIGH),
    ],
)
def test_service_list_valid_filters_on_empty_database(
    db_session: Session,
    status: WorkItemStatus | None,
    priority: WorkItemPriority | None,
) -> None:
    assert (
        work_item_service.list_work_items(db_session, status=status, priority=priority)
        == []
    )


def test_service_list_filter_optional_arguments_preserve_db_only_call(
    db_session: Session,
) -> None:
    created = _create_work_item(db_session)

    assert work_item_service.list_work_items(db_session) == [created]
    assert work_item_service.list_work_items(db_session, None, None) == [created]


def test_service_get_existing_and_missing_item(db_session: Session) -> None:
    created = _create_work_item(db_session)

    assert work_item_service.get_work_item(db_session, created.id) == created
    assert work_item_service.get_work_item(db_session, 999) is None


def test_service_update_existing_item(db_session: Session) -> None:
    created = _create_work_item(db_session)
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
    assert updated.metadata_json == {"estimate": 3, "reviewed": True}
    assert updated.created_at == original_created_at
    assert updated.updated_at is not None
    assert updated.updated_at >= original_updated_at


def test_service_update_preserves_unprovided_fields(db_session: Session) -> None:
    created = _create_work_item(db_session)

    updated = work_item_service.update_work_item(
        db_session,
        created.id,
        WorkItemUpdate(status="in_progress"),
    )

    assert updated is not None
    assert updated.status == "in_progress"
    assert updated.title == created.title
    assert updated.description == created.description
    assert updated.priority == created.priority
    assert updated.type == created.type
    assert updated.source == created.source
    assert updated.tags == ["release", "checklist"]
    assert updated.metadata_json == {"estimate": 2, "reviewed": False}


def test_service_update_missing_item_returns_none(db_session: Session) -> None:
    assert (
        work_item_service.update_work_item(
            db_session,
            999,
            WorkItemUpdate(status="done"),
        )
        is None
    )


def test_service_delete_existing_item(db_session: Session) -> None:
    created = _create_work_item(db_session)

    assert work_item_service.delete_work_item(db_session, created.id) is True
    assert work_item_service.get_work_item(db_session, created.id) is None
    assert work_item_service.list_work_items(db_session) == []


def test_service_delete_missing_item_returns_false(db_session: Session) -> None:
    assert work_item_service.delete_work_item(db_session, 999) is False
