from fastapi.testclient import TestClient


def test_health_check_returns_success(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "micro-api-work-items",
    }
