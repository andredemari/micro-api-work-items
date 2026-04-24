from typing import Any

from fastapi.testclient import TestClient


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
