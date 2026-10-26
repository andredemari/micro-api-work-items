from contextlib import closing
from copy import deepcopy
from datetime import datetime
import json
import sqlite3

import pytest

pytestmark = [pytest.mark.system, pytest.mark.api]


def _json(value):
    return json.dumps(value, sort_keys=True)


def _assert_created(response, payload):
    """Validate the contract before using a response as the restart baseline."""
    assert response.status_code == 201
    created = response.json()
    expected = {
        "title": payload["title"], "description": "", "status": "open",
        "priority": "medium", "type": "task", "source": "manual",
        "tags": [], "metadata": None, **payload,
    }
    assert set(created) == set(expected) | {"id", "created_at", "updated_at"}
    assert _json({key: created[key] for key in expected}) == _json(expected)
    assert type(created["id"]) is int
    assert created["id"] > 0
    for field in ("created_at", "updated_at"):
        assert isinstance(created[field], str)
        datetime.fromisoformat(created[field])
    return created


def _get(server, path, **kwargs):
    response = server.client.get(path, **kwargs)
    assert response.status_code == 200
    return response.json()


def _stored_rows(server):
    # Independent read-only oracle on the fixture-owned SQLite, never the runtime DB.
    with closing(sqlite3.connect(server.database.as_uri() + "?mode=ro", uri=True)) as db:
        return db.execute("SELECT * FROM work_items ORDER BY id").fetchall()


def _assert_error(response, field, kind, value):
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert len(errors) == 1
    assert {key: errors[0][key] for key in ("loc", "type", "input")} == {
        "loc": ["body", field], "type": kind, "input": value,
    }


def test_real_http_journey_and_invalid_request_no_write(http_process):
    # SYS-JOURNEY: real HTTP plus independently read stored rows.
    server = http_process.start()
    payload = {"title": "Synthetic journey", "status": "open", "priority": "high", "metadata": {"nested": [False, 0, "value"]}}
    response = server.client.post("/work-items", json=payload)
    created = _assert_created(response, payload)
    assert _json(_get(server, f"/work-items/{created['id']}")) == _json(created)
    response = server.client.patch(f"/work-items/{created['id']}", json={"status": "done", "priority": "low"})
    assert response.status_code == 200
    updated = response.json()
    assert _json(updated) == _json({**created, "status": "done", "priority": "low", "updated_at": updated["updated_at"]})
    assert _get(server, "/work-items", params={"status": "open", "priority": "high"}) == []
    assert _json(_get(server, "/work-items", params={"status": "done", "priority": "low"})) == _json([updated])
    before = deepcopy(_get(server, "/work-items"))
    assert _json(before) == _json([updated])
    stored_before = _stored_rows(server)
    rejected = server.client.patch(f"/work-items/{created['id']}", json={"priority": "urgent"})
    _assert_error(rejected, "priority", "enum", "urgent")
    assert _json(_get(server, "/work-items")) == _json(before)
    assert _stored_rows(server) == stored_before
    rejected = server.client.post("/work-items", json={"title": ""})
    _assert_error(rejected, "title", "string_too_short", "")
    assert _json(_get(server, "/work-items")) == _json(before)
    assert _stored_rows(server) == stored_before


def test_normal_restart_preserves_complete_objects(http_process):
    # SYS-RESTART: normal termination only, no crash/durability claim.
    server = http_process.start()
    payload = {"title": "Synthetic persistent record", "metadata": {"evidence": [1, False]}}
    response = server.client.post("/work-items", json=payload)
    created = _assert_created(response, payload)
    before = _get(server, "/work-items")
    assert _json(before) == _json([created])
    stored_before = _stored_rows(server)
    old_pid = server.process.pid
    server.stop()
    assert server.stops[-1]["normal"] is True
    server.start()
    assert server.process.pid != old_pid
    assert _json(_get(server, "/work-items")) == _json(before)
    assert _json(_get(server, f"/work-items/{created['id']}")) == _json(created)
    assert _stored_rows(server) == stored_before
