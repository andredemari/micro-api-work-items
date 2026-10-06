# Backlog

This backlog keeps the MVP small and traceable for the academic submission.

## Release 1: Core

| ID | Type | Item | Acceptance criteria |
| --- | --- | --- | --- |
| RF-01 | Functional | Health check | `GET /health` returns a successful JSON response. |
| RF-02 | Functional | Create work item | `POST /work-items` persists a valid work item and returns `201`. |
| RF-03 | Functional | List work items | `GET /work-items` returns persisted work items in ascending ID order; optional scalar `status` and `priority` enums combine with AND. Omitted filters do not restrict; no matches or an empty database return `200` with `[]`. Invalid, empty, or literal `null` values return `422` at the query parameter; repeated parameters use and validate the last occurrence. Queries preserve stored data and timestamps. |
| RF-04 | Functional | Retrieve work item | `GET /work-items/{id}` returns an existing item or `404`. |
| RF-05 | Functional | Update work item | `PATCH /work-items/{id}` partially updates status, priority, or other allowed fields. |
| RF-06 | Functional | Delete work item | `DELETE /work-items/{id}` removes an item and returns `204`. |
| RF-07 | Functional | Classify work item | `POST /work-items/classify` returns deterministic suggestions without persistence. |

## Release 2: Quality

| ID | Type | Item | Acceptance criteria |
| --- | --- | --- | --- |
| RNF-01 | Non-functional | Local-first persistence | The API runs locally with SQLite and no external services. |
| RNF-02 | Non-functional | Validation | Pydantic validates enum fields, required title, tags, and metadata shape. |
| RNF-03 | Non-functional | Automated tests | Tests cover health, CRUD, validation errors, list filters and query validation, repeated scalar parameters, ascending ID ordering, data preservation, missing items, timestamps, metadata, tags, and classification. |
| RNF-04 | Non-functional | Public-safe configuration | No credentials, external AI provider variables, or private context are required. |
| RNF-05 | Non-functional | Documentation | README and docs explain setup, architecture, decisions, prompt traceability, and limitations. |

## Release 3: Final Delivery

| ID | Type | Item | Acceptance criteria |
| --- | --- | --- | --- |
| RT-01 | Release task | Academic context | README identifies the course context and maps the task API idea to work items. |
| RT-02 | Release task | License | Repository includes an Apache License 2.0. |
| RT-03 | Release task | Diagrams | Architecture docs include Mermaid diagrams for layers, CRUD flow, and classifier flow. |
| RT-04 | Release task | Presentation readiness | README and supporting docs provide enough information for a short technical walkthrough. |
| RT-05 | Release task | Release checklist | Final checks are listed in `docs/release_checklist.md`. |
| RT-06 | Release task | Clean repository | No database, cache, `.env`, or local artifact files are tracked by Git. |
