from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.work_item_model import WorkItem
from app.schemas.work_items import WorkItemPriority, WorkItemStatus
from conftest import TestingSessionLocal


def _work_item_payload(**overrides: Any) -> dict[str, Any]:
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
    return payload


def _create_work_item(client: TestClient, **overrides: Any) -> dict[str, Any]:
    response = client.post("/work-items", json=_work_item_payload(**overrides))

    assert response.status_code == 201
    return response.json()


def test_list_work_items_starts_empty(client: TestClient) -> None:
    response = client.get("/work-items")

    assert response.status_code == 200
    assert response.json() == []


def test_list_work_items_returns_created_items(client: TestClient) -> None:
    created = _create_work_item(client)

    response = client.get("/work-items")

    assert response.status_code == 200
    assert response.json() == [created]


def test_create_work_item_returns_201_and_defaults(client: TestClient) -> None:
    response = client.post("/work-items", json={"title": "Prepare release checklist"})

    assert response.status_code == 201
    created = response.json()
    assert created["id"] == 1
    assert created["title"] == "Prepare release checklist"
    assert created["description"] == ""
    assert created["status"] == "open"
    assert created["priority"] == "medium"
    assert created["type"] == "task"
    assert created["source"] == "manual"
    assert created["tags"] == []
    assert created["metadata"] is None
    assert created["created_at"]
    assert created["updated_at"]


def test_create_work_item_persists_tags_and_metadata(client: TestClient) -> None:
    created = _create_work_item(client)

    assert created["tags"] == ["release", "checklist"]
    assert created["metadata"] == {"estimate": 2, "reviewed": False}


def test_get_work_item_by_id_returns_item(client: TestClient) -> None:
    created = _create_work_item(client)

    response = client.get(f"/work-items/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_patch_work_item_updates_status_priority_and_metadata(
    client: TestClient,
) -> None:
    created = _create_work_item(client)

    response = client.patch(
        f"/work-items/{created['id']}",
        json={
            "status": "in_progress",
            "priority": "high",
            "metadata": {"estimate": 3, "reviewed": True},
        },
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["status"] == "in_progress"
    assert updated["priority"] == "high"
    assert updated["metadata"] == {"estimate": 3, "reviewed": True}
    assert updated["created_at"] == created["created_at"]
    assert updated["updated_at"] >= created["updated_at"]


def test_patch_work_item_preserves_unprovided_fields(client: TestClient) -> None:
    created = _create_work_item(client)

    response = client.patch(
        f"/work-items/{created['id']}",
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated["status"] == "in_progress"
    assert updated["title"] == created["title"]
    assert updated["description"] == created["description"]
    assert updated["priority"] == created["priority"]
    assert updated["type"] == created["type"]
    assert updated["source"] == created["source"]
    assert updated["tags"] == created["tags"]
    assert updated["metadata"] == created["metadata"]


def test_delete_work_item_removes_item(client: TestClient) -> None:
    created = _create_work_item(client)

    response = client.delete(f"/work-items/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/work-items/{created['id']}").status_code == 404
    list_response = client.get("/work-items")
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_invalid_enum_values_return_validation_errors(client: TestClient) -> None:
    response = client.post(
        "/work-items",
        json={"title": "Invalid work item", "status": "waiting"},
    )

    assert response.status_code == 422


def test_missing_required_title_returns_validation_error(client: TestClient) -> None:
    response = client.post("/work-items", json={"status": "open"})

    assert response.status_code == 422


def test_missing_work_item_returns_404(client: TestClient) -> None:
    assert client.get("/work-items/999").status_code == 404
    assert client.patch("/work-items/999", json={"status": "done"}).status_code == 404
    assert client.delete("/work-items/999").status_code == 404


@pytest.fixture()
def filter_items(client: TestClient) -> list[dict[str, Any]]:
    return [
        _create_work_item(client, title=title, status=status, priority=priority)
        for title, status, priority in (
            ("A", "open", "high"),
            ("B", "open", "low"),
            ("C", "done", "high"),
            ("D", "in_progress", "critical"),
        )
    ]


@pytest.mark.parametrize(
    ("query", "expected_indexes"),
    [
        ("", [0, 1, 2, 3]),
        ("status=open", [0, 1]),
        ("priority=high", [0, 2]),
        ("status=open&priority=high", [0]),
        ("status=archived", []),
        ("priority=medium", []),
        ("status=archived&priority=critical", []),
        ("status=done&status=open", [0, 1]),
        ("priority=low&priority=high", [0, 2]),
        ("status=done&status=open&priority=low&priority=high", [0]),
        ("status=testing&status=open", [0, 1]),
        ("status=&status=open", [0, 1]),
        ("status=null&status=open", [0, 1]),
        ("priority=urgent&priority=high", [0, 2]),
        ("priority=&priority=high", [0, 2]),
        ("priority=null&priority=high", [0, 2]),
    ],
)
def test_list_filters_match_acceptance_examples(
    client: TestClient,
    filter_items: list[dict[str, Any]],
    query: str,
    expected_indexes: list[int],
) -> None:
    response = client.get(f"/work-items?{query}")

    assert response.status_code == 200
    assert response.json() == [filter_items[index] for index in expected_indexes]


@pytest.mark.parametrize("status", list(WorkItemStatus))
@pytest.mark.parametrize("priority", list(WorkItemPriority))
def test_list_filters_accept_all_enum_combinations(
    client: TestClient,
    status: WorkItemStatus,
    priority: WorkItemPriority,
) -> None:
    created = _create_work_item(client, status=status, priority=priority)
    other_status = next(value for value in WorkItemStatus if value != status)
    other_priority = next(value for value in WorkItemPriority if value != priority)
    _create_work_item(client, status=other_status, priority=other_priority)

    for query in (
        f"status={status.value}",
        f"priority={priority.value}",
        f"status={status.value}&priority={priority.value}",
    ):
        response = client.get(f"/work-items?{query}")
        assert response.status_code == 200
        assert response.json() == [created]


@pytest.mark.parametrize(
    "query",
    ["status=open", "priority=high", "status=open&priority=high"],
)
def test_list_filters_return_empty_on_empty_database(
    client: TestClient, query: str,
) -> None:
    response = client.get(f"/work-items?{query}")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(
    ("parameter", "invalid_value", "valid_value"),
    [
        ("status", "testing", "open"),
        ("status", "", "open"),
        ("status", "null", "open"),
        ("priority", "urgent", "high"),
        ("priority", "", "high"),
        ("priority", "null", "high"),
    ],
)
@pytest.mark.parametrize("repeated", [False, True])
def test_list_filters_reject_invalid_last_value(
    client: TestClient,
    filter_items: list[dict[str, Any]],
    parameter: str,
    invalid_value: str,
    valid_value: str,
    repeated: bool,
) -> None:
    query = f"{parameter}={invalid_value}"
    if repeated:
        query = f"{parameter}={valid_value}&{query}"

    response = client.get(f"/work-items?{query}")

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) == 1
    assert errors[0]["loc"] == ["query", parameter]
    assert errors[0]["input"] == invalid_value


def test_list_filters_report_both_invalid_parameters(client: TestClient) -> None:
    response = client.get("/work-items?status=open&status=&priority=high&priority=null")

    assert response.status_code == 422
    assert {tuple(error["loc"]) for error in response.json()["detail"]} == {
        ("query", "status"), ("query", "priority"),
    }


def test_list_filters_preserve_persisted_data_after_repeated_queries(
    client: TestClient, filter_items: list[dict[str, Any]],
) -> None:
    def snapshot() -> list[dict[str, Any]]:
        with TestingSessionLocal() as db:
            return [
                {column.key: getattr(item, column.key) for column in WorkItem.__mapper__.column_attrs}
                for item in db.scalars(select(WorkItem).order_by(WorkItem.id))
            ]

    before = snapshot()
    for _ in range(3):
        for query, expected in (
            ("", filter_items),
            ("status=open", filter_items[:2]),
            ("priority=high", [filter_items[0], filter_items[2]]),
            ("status=open&priority=high", [filter_items[0]]),
            ("status=archived&priority=critical", []),
            ("status=done&status=open", filter_items[:2]),
        ):
            response = client.get(f"/work-items?{query}")
            assert response.status_code == 200
            assert response.json() == expected
        for query in ("status=testing", "priority=", "status=null"):
            assert client.get(f"/work-items?{query}").status_code == 422

    assert snapshot() == before
    for created in filter_items:
        response = client.get(f"/work-items/{created['id']}")
        assert response.status_code == 200
        assert response.json() == created


def test_list_filters_openapi_declares_optional_scalar_enums(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    parameters = schema["paths"]["/work-items"]["get"]["parameters"]

    assert {parameter["name"] for parameter in parameters} == {"status", "priority"}
    for parameter in parameters:
        assert parameter["in"] == "query"
        assert parameter["required"] is False
        variants = parameter["schema"]["anyOf"]
        enum_ref = next(variant["$ref"] for variant in variants if "$ref" in variant)
        enum_schema = schema["components"]["schemas"][enum_ref.rsplit("/", 1)[1]]
        enum_type = WorkItemStatus if parameter["name"] == "status" else WorkItemPriority
        assert enum_schema["type"] == "string"
        assert enum_schema["enum"] == [value.value for value in enum_type]
