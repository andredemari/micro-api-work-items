from typing import Any

import pytest
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.models.work_item_model import WorkItem
from app.repositories import work_item_repository
from app.schemas.work_items import WorkItemPriority, WorkItemRead, WorkItemStatus


def _work_item_values(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "title": "Prepare release checklist",
        "description": "Create a short checklist for the next release.",
        "status": "open",
        "priority": "medium",
        "type": "task",
        "source": "manual",
        "tags": ["release", "checklist"],
        "metadata_json": {"estimate": 2, "reviewed": False},
    }
    values.update(overrides)
    return values


def _create_work_item(db_session: Session, **overrides: Any):
    return work_item_repository.create_work_item(
        db_session,
        _work_item_values(**overrides),
    )


def test_repository_list_starts_empty(db_session: Session) -> None:
    assert work_item_repository.list_work_items(db_session) == []


def test_repository_create_work_item_persists_fields(db_session: Session) -> None:
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


def test_repository_list_returns_multiple_items(db_session: Session) -> None:
    first = _create_work_item(db_session, title="First work item")
    second = _create_work_item(db_session, title="Second work item")

    assert work_item_repository.list_work_items(db_session) == [first, second]


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
def test_repository_list_filters(
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

    listed = work_item_repository.list_work_items(
        db_session, status=status, priority=priority
    )

    assert listed == [item for item in items if item.title in expected_titles]
    assert [item.title for item in listed] == expected_titles


@pytest.mark.parametrize("status", list(WorkItemStatus))
def test_repository_list_filters_accept_each_status(
    db_session: Session, status: WorkItemStatus
) -> None:
    items = [
        _create_work_item(db_session, title=value.value, status=value)
        for value in WorkItemStatus
    ]

    assert work_item_repository.list_work_items(db_session, status=status) == [
        item for item in items if item.status == status
    ]


@pytest.mark.parametrize("priority", list(WorkItemPriority))
def test_repository_list_filters_accept_each_priority(
    db_session: Session, priority: WorkItemPriority
) -> None:
    items = [
        _create_work_item(db_session, title=value.value, priority=value)
        for value in WorkItemPriority
    ]

    assert work_item_repository.list_work_items(db_session, priority=priority) == [
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
def test_repository_list_valid_filters_on_empty_database(
    db_session: Session,
    status: WorkItemStatus | None,
    priority: WorkItemPriority | None,
) -> None:
    assert (
        work_item_repository.list_work_items(
            db_session, status=status, priority=priority
        )
        == []
    )


def test_repository_list_filter_optional_arguments_preserve_db_only_call(
    db_session: Session,
) -> None:
    created = _create_work_item(db_session)

    assert work_item_repository.list_work_items(db_session) == [created]
    assert work_item_repository.list_work_items(db_session, None, None) == [created]


@pytest.mark.parametrize(
    ("status", "priority", "expected_ids"),
    [
        (None, None, [1, 2, 3, 4, 5]),
        (WorkItemStatus.OPEN, None, [1, 2, 5]),
        (None, WorkItemPriority.HIGH, [1, 3, 5]),
        (WorkItemStatus.OPEN, WorkItemPriority.HIGH, [1, 5]),
    ],
)
def test_repository_list_filters_order_ids_when_unordered_select_is_reversed(
    db_session: Session,
    status: WorkItemStatus | None,
    priority: WorkItemPriority | None,
    expected_ids: list[int],
) -> None:
    # Titles differ from ID order, including both items matching open/high.
    for title, item_status, item_priority in [
        ("Zulu", "open", "high"),
        ("Echo", "open", "low"),
        ("Delta", "done", "high"),
        ("Bravo", "in_progress", "critical"),
        ("Alpha", "open", "high"),
    ]:
        _create_work_item(
            db_session, title=title, status=item_status, priority=item_priority
        )

    unordered_statement = select(WorkItem.id)
    if status is not None:
        unordered_statement = unordered_statement.where(WorkItem.status == status)
    if priority is not None:
        unordered_statement = unordered_statement.where(WorkItem.priority == priority)

    db_session.execute(text("PRAGMA reverse_unordered_selects=ON"))
    try:
        # Prove the fixture cannot satisfy ascending order without ORDER BY.
        assert list(db_session.scalars(unordered_statement)) == expected_ids[::-1]
        if status is None and priority is None:
            listed = work_item_repository.list_work_items(db_session)
        else:
            listed = work_item_repository.list_work_items(
                db_session, status=status, priority=priority
            )
        assert [item.id for item in listed] == expected_ids
    finally:
        db_session.execute(text("PRAGMA reverse_unordered_selects=OFF"))


def test_repository_repeated_filters_preserve_persisted_data(
    db_session: Session,
) -> None:
    _create_work_item(db_session, title="A", status="open", priority="high")
    _create_work_item(db_session, title="B", status="open", priority="low")
    _create_work_item(db_session, title="C", status="done", priority="high")
    _create_work_item(
        db_session, title="D", status="in_progress", priority="critical"
    )
    before = [
        WorkItemRead.model_validate(item).model_dump()
        for item in db_session.scalars(select(WorkItem).order_by(WorkItem.id))
    ]

    for _ in range(3):
        work_item_repository.list_work_items(db_session)
        work_item_repository.list_work_items(db_session, status=WorkItemStatus.OPEN)
        work_item_repository.list_work_items(db_session, priority=WorkItemPriority.HIGH)
        work_item_repository.list_work_items(
            db_session, status=WorkItemStatus.OPEN, priority=WorkItemPriority.HIGH
        )
        work_item_repository.list_work_items(
            db_session, status=WorkItemStatus.ARCHIVED, priority=WorkItemPriority.CRITICAL
        )

    db_session.expire_all()
    after = [
        WorkItemRead.model_validate(item).model_dump()
        for item in db_session.scalars(select(WorkItem).order_by(WorkItem.id))
    ]
    assert after == before


def test_repository_get_existing_and_missing_item(db_session: Session) -> None:
    created = _create_work_item(db_session)

    assert work_item_repository.get_work_item(db_session, created.id) == created
    assert work_item_repository.get_work_item(db_session, 999) is None


def test_repository_update_existing_item(db_session: Session) -> None:
    created = _create_work_item(db_session)
    original_created_at = created.created_at
    original_updated_at = created.updated_at

    updated = work_item_repository.update_work_item(
        db_session,
        created.id,
        {
            "status": "in_progress",
            "priority": "high",
            "metadata_json": {"estimate": 3, "reviewed": True},
        },
    )

    assert updated is not None
    assert updated.status == "in_progress"
    assert updated.priority == "high"
    assert updated.metadata_json == {"estimate": 3, "reviewed": True}
    assert updated.created_at == original_created_at
    assert updated.updated_at is not None
    assert updated.updated_at >= original_updated_at


def test_repository_update_preserves_unprovided_fields(db_session: Session) -> None:
    created = _create_work_item(db_session)

    updated = work_item_repository.update_work_item(
        db_session,
        created.id,
        {"status": "in_progress"},
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


def test_repository_update_missing_item_returns_none(db_session: Session) -> None:
    assert (
        work_item_repository.update_work_item(
            db_session,
            999,
            {"status": "done"},
        )
        is None
    )


def test_repository_delete_existing_item(db_session: Session) -> None:
    created = _create_work_item(db_session)

    assert work_item_repository.delete_work_item(db_session, created.id) is True
    assert work_item_repository.get_work_item(db_session, created.id) is None
    assert work_item_repository.list_work_items(db_session) == []


def test_repository_delete_missing_item_returns_false(db_session: Session) -> None:
    assert work_item_repository.delete_work_item(db_session, 999) is False
