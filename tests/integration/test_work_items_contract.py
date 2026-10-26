from copy import deepcopy
from datetime import datetime
import json
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models.work_item_model import WorkItem
from conftest import TestingSessionLocal


pytestmark = [pytest.mark.integration, pytest.mark.api, pytest.mark.functional]


def _payload(**overrides: Any) -> dict[str, Any]:
    payload = {
        "title": "Prepare research notes",
        "description": "Preserve this description.",
        "status": "open",
        "priority": "high",
        "type": "research",
        "source": "other",
        "tags": ["research", "preserve"],
        "metadata": {
            "nested": {
                "values": [None, False, 0, 1.25, "ação", {"ready": True}],
                "empty": {},
            },
            "empty_list": [],
        },
    }
    payload.update(overrides)
    return payload


def _snapshot() -> list[dict[str, Any]]:
    """Read committed rows through a fresh session on the existing test engine."""
    with TestingSessionLocal() as db:
        result = []
        for item in db.scalars(select(WorkItem).order_by(WorkItem.id)):
            values = {
                column.key: deepcopy(getattr(item, column.key))
                for column in WorkItem.__mapper__.column_attrs
            }
            values["metadata"] = values.pop("metadata_json")
            for field in ("created_at", "updated_at"):
                values[field] = values[field].isoformat()
            result.append(values)
        return result


def _create(client: TestClient, **overrides: Any) -> dict[str, Any]:
    payload = _payload(**overrides)
    response = client.post("/work-items", json=payload)

    assert response.status_code == 201
    created = response.json()
    assert set(created) == set(payload) | {"id", "created_at", "updated_at"}
    assert {field: created[field] for field in payload} == payload
    assert isinstance(created["id"], int)
    assert created["id"] > 0
    datetime.fromisoformat(created["created_at"])
    datetime.fromisoformat(created["updated_at"])
    return created


def _read(client: TestClient, item_id: int) -> dict[str, Any]:
    response = client.get(f"/work-items/{item_id}")
    assert response.status_code == 200
    return response.json()


def _assert_body_error(
    response: Any,
    location: tuple[str | int, ...],
    error_type: str,
    rejected_input: Any,
) -> None:
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert isinstance(errors, list)
    assert len(errors) == 1
    error = errors[0]
    assert error["loc"] == list(location)
    assert error["type"] == error_type
    assert error["input"] == rejected_input
    assert isinstance(error["msg"], str)
    assert error["msg"]


def test_nested_metadata_roundtrip_and_omitted_patch_fields(
    client: TestClient,
) -> None:
    created = _create(client)
    expected_metadata = _payload()["metadata"]

    assert _read(client, created["id"]) == created
    assert _snapshot() == [created]

    # JSON comparison also distinguishes booleans from numeric replacements.
    expected_json = json.dumps(expected_metadata, sort_keys=True)
    assert json.dumps(created["metadata"], sort_keys=True) == expected_json
    assert (
        json.dumps(_snapshot()[0]["metadata"], sort_keys=True)
        == expected_json
    )

    response = client.patch(
        f"/work-items/{created['id']}",
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated == {
        **created,
        "status": "in_progress",
        "updated_at": updated["updated_at"],
    }
    assert (
        datetime.fromisoformat(updated["updated_at"])
        >= datetime.fromisoformat(created["updated_at"])
    )
    assert _read(client, created["id"]) == updated
    assert _snapshot() == [updated]
    assert (
        json.dumps(_snapshot()[0]["metadata"], sort_keys=True)
        == expected_json
    )


def test_filters_use_values_after_committed_patch(client: TestClient) -> None:
    target = _create(client, title="Target")
    other = _create(
        client,
        title="Unrelated",
        status="done",
        priority="high",
    )

    before = client.get(
        "/work-items", params={"status": "open", "priority": "high"}
    )
    assert before.status_code == 200
    assert before.json() == [target]

    response = client.patch(
        f"/work-items/{target['id']}",
        json={"status": "done", "priority": "low"},
    )

    assert response.status_code == 200
    updated = response.json()
    assert updated == {
        **target,
        "status": "done",
        "priority": "low",
        "updated_at": updated["updated_at"],
    }
    assert _snapshot() == [updated, other]

    for parameters, expected in (
        ({"status": "open", "priority": "high"}, []),
        ({"status": "done", "priority": "low"}, [updated]),
        ({"status": "done"}, [updated, other]),
        ({"priority": "high"}, [other]),
    ):
        listed = client.get("/work-items", params=parameters)
        assert listed.status_code == 200
        assert listed.json() == expected

    assert _read(client, target["id"]) == updated
    assert _snapshot() == [updated, other]


def test_classification_preserves_preexisting_record(
    client: TestClient,
) -> None:
    created = _create(
        client,
        title="Critical incident",
        description="Service unavailable for users.",
        tags=["Ops"],
        type="research",
        priority="low",
    )
    before = _snapshot()

    response = client.post(
        "/work-items/classify",
        json={
            field: created[field]
            for field in ("title", "description", "tags")
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "suggested_type": "incident",
        "suggested_priority": "critical",
        "suggested_tags": ["ops", "incident", "critical"],
        "reasons": [
            "type matched keyword: incident",
            "priority matched keyword: critical",
        ],
    }
    assert _snapshot() == before
    assert _read(client, created["id"]) == created


@pytest.mark.parametrize("method", ["post", "patch"])
@pytest.mark.parametrize("length", [0, 1, 2, 199, 200, 201])
def test_title_boundaries(
    client: TestClient, method: str, length: int,
) -> None:
    unrelated = _create(client, title="Unrelated")
    target = _create(client, title="Original") if method == "patch" else None
    before = _snapshot()
    title = "x" * length

    if method == "post":
        payload = _payload(title=title)
        response = client.post("/work-items", json=payload)
    else:
        assert target is not None
        payload = {"title": title}
        response = client.patch(
            f"/work-items/{target['id']}", json=payload
        )

    if length in (0, 201):
        _assert_body_error(
            response,
            ("body", "title"),
            "string_too_short" if length == 0 else "string_too_long",
            title,
        )
        assert _snapshot() == before
        assert _read(client, unrelated["id"]) == unrelated
        if target is not None:
            assert _read(client, target["id"]) == target
        return

    assert response.status_code == (201 if method == "post" else 200)
    changed = response.json()
    assert changed["title"] == title

    if target is None:
        assert set(changed) == set(payload) | {
            "id", "created_at", "updated_at"
        }
        assert {field: changed[field] for field in payload} == payload
    else:
        assert changed == {
            **target,
            "title": title,
            "updated_at": changed["updated_at"],
        }

    assert _read(client, changed["id"]) == changed
    assert _snapshot() == [unrelated, changed]


@pytest.mark.parametrize("method", ["post", "patch"])
@pytest.mark.parametrize(
    ("changes", "location", "error_type", "rejected_input"),
    [
        pytest.param(
            {"status": "waiting"}, ("body", "status"), "enum", "waiting",
            id="status-enum",
        ),
        pytest.param(
            {"priority": "urgent"}, ("body", "priority"), "enum", "urgent",
            id="priority-enum",
        ),
        pytest.param(
            {"type": "unknown"}, ("body", "type"), "enum", "unknown",
            id="type-enum",
        ),
        pytest.param(
            {"source": "unknown"}, ("body", "source"), "enum", "unknown",
            id="source-enum",
        ),
        pytest.param(
            {"tags": [1]}, ("body", "tags", 0), "string_type", 1,
            id="tags-member",
        ),
        pytest.param(
            {"metadata": ["invalid"]},
            ("body", "metadata"),
            "dict_type",
            ["invalid"],
            id="metadata-container",
        ),
    ],
)
def test_invalid_body_is_localized_and_does_not_write(
    client: TestClient,
    method: str,
    changes: dict[str, Any],
    location: tuple[str | int, ...],
    error_type: str,
    rejected_input: Any,
) -> None:
    created = _create(client)
    before = _snapshot()

    if method == "post":
        response = client.post("/work-items", json=_payload(**changes))
    else:
        response = client.patch(
            f"/work-items/{created['id']}", json=changes
        )

    _assert_body_error(response, location, error_type, rejected_input)
    assert _snapshot() == before
    assert _read(client, created["id"]) == created


@pytest.mark.parametrize(
    ("payload", "error_type", "rejected_input"),
    [
        pytest.param({}, "missing", {}, id="missing"),
        pytest.param(
            {"title": None}, "string_type", None, id="null-on-create"
        ),
    ],
)
def test_create_requires_non_null_title_without_writing(
    client: TestClient,
    payload: dict[str, Any],
    error_type: str,
    rejected_input: Any,
) -> None:
    created = _create(client)
    before = _snapshot()

    response = client.post("/work-items", json=payload)

    _assert_body_error(
        response, ("body", "title"), error_type, rejected_input
    )
    assert _snapshot() == before
    assert _read(client, created["id"]) == created


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_id_preserves_unrelated_item(
    client: TestClient, method: str,
) -> None:
    created = _create(client)
    before = _snapshot()
    path = f"/work-items/{created['id'] + 1000}"

    if method == "patch":
        response = client.patch(path, json={"status": "done"})
    else:
        response = client.request(method, path)

    assert response.status_code == 404
    assert response.json() == {"detail": "Work item not found."}
    assert _snapshot() == before
    assert _read(client, created["id"]) == created
