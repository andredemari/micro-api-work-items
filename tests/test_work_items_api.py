from fastapi.testclient import TestClient


def test_create_list_get_patch_and_delete_work_item(client: TestClient) -> None:
    create_payload = {
        "title": "Prepare release checklist",
        "description": "Create a short checklist for the next release.",
        "status": "open",
        "priority": "medium",
        "type": "task",
        "source": "manual",
        "tags": ["release", "checklist"],
        "metadata": {"estimate": 2, "reviewed": False},
    }

    create_response = client.post("/work-items", json=create_payload)

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] == 1
    assert created["title"] == create_payload["title"]
    assert created["tags"] == ["release", "checklist"]
    assert created["metadata"] == {"estimate": 2, "reviewed": False}
    assert created["created_at"]
    assert created["updated_at"]

    list_response = client.get("/work-items")

    assert list_response.status_code == 200
    assert list_response.json() == [created]

    get_response = client.get("/work-items/1")

    assert get_response.status_code == 200
    assert get_response.json() == created

    patch_response = client.patch(
        "/work-items/1",
        json={
            "status": "in_progress",
            "priority": "high",
            "metadata": {"estimate": 3, "reviewed": True},
        },
    )

    assert patch_response.status_code == 200
    updated = patch_response.json()
    assert updated["status"] == "in_progress"
    assert updated["priority"] == "high"
    assert updated["metadata"] == {"estimate": 3, "reviewed": True}
    assert updated["tags"] == ["release", "checklist"]
    assert updated["created_at"] == created["created_at"]
    assert updated["updated_at"] != created["updated_at"]

    delete_response = client.delete("/work-items/1")

    assert delete_response.status_code == 204
    assert client.get("/work-items/1").status_code == 404
    assert client.get("/work-items").json() == []


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
