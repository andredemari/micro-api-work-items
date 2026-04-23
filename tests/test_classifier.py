from fastapi.testclient import TestClient


def test_classifier_is_deterministic(client: TestClient) -> None:
    payload = {
        "title": "Critical incident with service outage",
        "description": "The service is unavailable for users.",
        "tags": ["support"],
    }

    first_response = client.post("/work-items/classify", json=payload)
    second_response = client.post("/work-items/classify", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json() == second_response.json()
    assert first_response.json()["suggested_type"] == "incident"
    assert first_response.json()["suggested_priority"] == "critical"
    assert first_response.json()["suggested_tags"] == [
        "support",
        "incident",
        "critical",
    ]


def test_classifier_does_not_persist_work_items(client: TestClient) -> None:
    assert client.get("/work-items").json() == []

    response = client.post(
        "/work-items/classify",
        json={
            "title": "Investigate low priority cleanup",
            "description": "Analyze whether this should become a future task.",
            "tags": [],
        },
    )

    assert response.status_code == 200
    assert client.get("/work-items").json() == []
