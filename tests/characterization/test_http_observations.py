"""Synthetic observations; completion does not approve product/security policy."""
import uuid

import pytest

pytestmark = [pytest.mark.system, pytest.mark.characterization]


def _capture(record, case_id, response):
    try:
        body = response.json()
    except ValueError:
        body = response.text
    packet = {"status": response.status_code, "body": body}
    record(case_id, packet)  # Preserve each completed step before subsequent failures.
    return packet


def _create(server, title, record):
    response = server.client.post("/work-items", json={"title": title})
    packet = _capture(record, "OBS-HTTP-SETUP", response)
    assert response.status_code == 201  # Existing setup contract only.
    return packet["body"]


def test_ordered_stale_clients(http_process, record_observation):
    server = http_process.start()
    created = _create(server, "Synthetic concurrent edit", record_observation)
    path = f"/work-items/{created['id']}"
    with server.new_client() as a, server.new_client() as b:
        base_a = _capture(record_observation, "OBS-CONCURRENCY-READ-A", a.get(path))
        base_b = _capture(record_observation, "OBS-CONCURRENCY-READ-B", b.get(path))
        assert base_a["status"] == base_b["status"] == 200
        assert base_a["body"] == base_b["body"] == created
        first = _capture(record_observation, "OBS-CONCURRENCY-WRITE-A", a.patch(path, json={"title": "Edit A"}))
        # Ordered completed requests, not a race or a fixed sleep.
        second = _capture(record_observation, "OBS-CONCURRENCY-WRITE-B", b.patch(path, json={"title": "Edit B"}))
    final = _capture(record_observation, "OBS-CONCURRENCY-FINAL", server.client.get(path))
    record_observation("OBS-HTTP-CONCURRENCY", {
        "same_initial_state": True, "first": first, "second": second, "final": final,
        "meaning": "Anonymous clients, not identities; no version-control or409 expectation.",
    })


def test_access_without_credentials(http_process, record_observation):
    server = http_process.start()
    with server.new_client() as anonymous:
        listed = anonymous.get("/work-items")
        listed_packet = _capture(record_observation, "OBS-AUTH-LIST", listed)
        created = anonymous.post("/work-items", json={"title": "Synthetic anonymous record"})
        created_packet = _capture(record_observation, "OBS-AUTH-CREATE", created)
        record_observation("OBS-HTTP-AUTH", {
            "authorization_header_sent": "authorization" in listed.request.headers,
            "list": listed_packet, "create": created_packet,
            "meaning": "Allowed access demonstrates no barrier in this flow, not a security pass.",
        })


class SyntheticResponseLost(RuntimeError):
    pass


def _write_then_discard(server, payload, record):
    response = server.client.post("/work-items", json=payload)
    audit = _capture(record, "OBS-REPETITION-CONFIRMED-WRITE-AUDIT", response)
    assert audit["status"] == 201
    raise SyntheticResponseLost("Synthetic client receives no response; audit retains confirmed write")


def test_discarded_response_and_explicit_repeated_post(http_process, record_observation):
    server = http_process.start()
    reference = uuid.uuid4().hex
    payload = {"title": "Synthetic repeated action", "metadata": {"client_reference": reference}}
    with pytest.raises(SyntheticResponseLost):
        _write_then_discard(server, payload, record_observation)
    # Reconcile from the submitted reference, without using the audit's returned ID.
    reconciled = _capture(record_observation, "OBS-REPETITION-RECONCILIATION", server.client.get("/work-items"))
    assert reconciled["status"] == 200
    recovered = [row for row in reconciled["body"] if row["metadata"] == payload["metadata"]]
    record_observation("OBS-REPETITION-QUERY-RESULT", {"matching_rows": recovered})
    repeated = _capture(record_observation, "OBS-REPETITION-EXPLICIT-RETRY", server.client.post("/work-items", json=payload))
    final = _capture(record_observation, "OBS-REPETITION-FINAL", server.client.get("/work-items"))
    matching = [row for row in final["body"] if row["metadata"] == payload["metadata"]] if isinstance(final["body"], list) else None
    record_observation("OBS-HTTP-REPETITION", {
        "query_before_repeat": recovered, "repeat": repeated, "final": final,
        "matching_rows": matching,
        "meaning": "Client-side discarded response after confirmed write; no real packet loss or idempotency implementation.",
    })
