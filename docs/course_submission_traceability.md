# Course Submission Traceability

This document maps the academic task expectations to repository artifacts for review and reproducibility.

| Course/core expectation | Repository evidence | Status | Notes |
| --- | --- | --- | --- |
| FastAPI application | `app/main.py` | Done | Application entrypoint wires the controllers and startup database initialization. |
| Health endpoint | `app/controllers/health_controller.py`, `tests/test_health.py` | Done | `GET /health` verifies the API is reachable. |
| Create work item endpoint | `app/controllers/work_item_controller.py`, `tests/test_work_items_api.py` | Done | `POST /work-items` creates persisted work items. |
| List work items endpoint | `app/controllers/work_item_controller.py`, `tests/test_work_items_api.py` | Done | `GET /work-items` returns persisted work items. |
| Get work item endpoint | `app/controllers/work_item_controller.py`, `tests/test_work_items_api.py` | Done | `GET /work-items/{id}` returns one item or `404`. |
| Update work item endpoint | `app/controllers/work_item_controller.py`, `tests/test_work_items_api.py` | Done | `PATCH /work-items/{id}` supports partial updates. |
| Delete work item endpoint | `app/controllers/work_item_controller.py`, `tests/test_work_items_api.py` | Done | `DELETE /work-items/{id}` removes one item or returns `404`. |
| Classification/PriorityAdvisor endpoint | `app/controllers/work_item_controller.py`, `app/services/priority_advisor.py`, `tests/test_classifier.py` | Done | `POST /work-items/classify` returns suggestions without persistence. |
| Pydantic schemas | `app/schemas/work_items.py` | Done | Request, response, enum, update, and classification contracts are explicit. |
| SQLite persistence | `app/db/database.py`, `app/models/work_item_model.py`, `data/.gitkeep` | Done | Runtime defaults to local SQLite under `data/`. |
| Service layer | `app/services/work_items.py`, `app/services/priority_advisor.py` | Done | Services keep application orchestration separate from controllers. |
| Repository layer | `app/repositories/work_item_repository.py`, `tests/test_work_item_repository.py` | Done | Persistence operations are isolated behind repository functions. |
| Automated tests | `tests/` | Done | Tests cover API, service, repository, provider, safety gate, and validation behavior. |
| Error handling for `404` and `422` | `tests/test_work_items_api.py`, `docs/api_examples.md` | Done | Missing records and invalid payloads are covered. |
| README setup/run/test instructions | `README.md` | Done | Includes Makefile, standard Python, Anaconda, PowerShell, and Linux/WSL paths. |
| Backlog and acceptance criteria | `docs/backlog.md`, `docs/mvp_scope.md`, `docs/refactor_backlog.md` | Done | MVP and refactor work are traceable through acceptance-oriented docs. |
| Mermaid/architecture documentation | `docs/architecture.md` | Done | Includes layered architecture and request-flow diagrams. |
| Prompt traceability | `docs/prompts.md` | Done | Sanitized lifecycle prompts support academic reproducibility. |
| Release checklist | `docs/release_checklist.md` | Done | Final submission checks are captured in one place. |
| Deterministic safety check | `scripts/safety_check.py`, `scripts/safety_policy.json`, `docs/security_checks.md`, `tests/test_safety_check.py` | Guarded | Safety checks are deterministic, non-destructive, and standard-library only. |
| External LLM provider runtime | `docs/external_provider_plan.md`, `docs/local_llm_setup.md` | Out of scope | Runtime remains local and deterministic; future provider work is documentation-only. |
| Credentials and runtime external AI provider | `.env.example`, `docs/information_governance.md`, `docs/security_checks.md` | Guarded | No provider credentials are required or configured for the MVP. |
