# Course Submission Traceability

This document maps the academic task expectations to repository artifacts for review and reproducibility.

| Course/core expectation | Repository evidence | Status | Notes |
| --- | --- | --- | --- |
| Initial project setup | `.gitignore`, `requirements.txt`, `Makefile`, Git history | Done | Python artifacts, local databases, environment files, and generated archives are ignored; commits use Conventional Commit style. |
| Local Python environment guidance | `README.md`, `.env.example` | Done | README covers standard Python, Anaconda, PowerShell, Linux/WSL, and Makefile interpreter override paths. |
| README reproducibility | `README.md` | Done | Includes objective, stack, setup, run, tests, limitations, API usage, and AI-assisted development notes. |
| FastAPI application | `app/main.py` | Done | Application entrypoint wires controllers and startup database initialization. |
| Health endpoint | `app/controllers/health_controller.py`, `tests/test_health.py` | Done | `GET /health` verifies the API is reachable. |
| CRUD endpoints for task/work item concept | `app/controllers/work_item_controller.py`, `tests/test_work_items_api.py` | Done | Course task operations are implemented with `/work-items` routes for create, list, get, update, and delete. |
| HTTP status codes and API errors | `tests/test_work_items_api.py`, `docs/api_examples.md` | Done | Tests and examples cover successful responses, `404` for missing items, and `422` for invalid payloads. |
| Classification/PriorityAdvisor endpoint | `app/controllers/work_item_controller.py`, `app/services/priority_advisor.py`, `tests/test_classifier.py` | Done | `POST /work-items/classify` returns suggestions without persistence. |
| Controllers layer | `app/controllers/` | Done | FastAPI route handlers are separated from services and persistence. |
| Schemas/Pydantic API contracts | `app/schemas/work_items.py` | Done | Request, response, enum, update, and classification contracts are explicit. |
| Models/SQLAlchemy persistence model | `app/models/work_item_model.py` | Done | ORM model remains distinct from Pydantic API schemas. |
| Services layer | `app/services/` | Done | Services keep application orchestration separate from controllers. |
| Repositories layer | `app/repositories/work_item_repository.py`, `tests/test_work_item_repository.py` | Done | Persistence operations are isolated behind repository functions. |
| Database/session setup | `app/db/database.py` | Done | SQLite engine, session lifecycle, schema initialization, and local data directory creation are centralized. |
| Local deterministic PriorityAdvisor | `app/services/priority_advisor.py`, `app/providers/priority/local_provider.py` | Done | Classification is deterministic and local; no runtime provider call is required. |
| SQLite local persistence | `app/db/database.py`, `data/.gitkeep` | Done | Runtime defaults to `sqlite:///./data/work_items.db`. |
| Ignored runtime database files | `.gitignore`, `docs/security_checks.md` | Guarded | Database files are ignored and checked before submission. |
| Reproducible reset behavior | `README.md` | Done | README explains how to reset local SQLite state by removing `data/work_items.db`. |
| API route tests | `tests/test_work_items_api.py`, `tests/test_health.py`, `tests/test_classifier.py` | Done | Tests cover health, CRUD routes, classification route, non-persistence, and API error cases. |
| Service tests | `tests/test_work_items_service.py`, `tests/test_priority_advisor_service.py` | Done | Tests cover direct service behavior and PriorityAdvisor behavior. |
| Repository tests | `tests/test_work_item_repository.py` | Done | Tests cover direct persistence operations and missing-item contracts. |
| PriorityAdvisor/local provider tests | `tests/test_priority_advisor_service.py`, `tests/test_local_priority_provider.py` | Done | Tests cover deterministic classification and local provider output. |
| Validation/error tests | `tests/test_work_items_api.py` | Done | Tests cover invalid enums, missing required title, and missing item cases. |
| Deterministic safety-check tests | `tests/test_safety_check.py` | Guarded | Tests cover non-destructive safety gate behavior with temporary Git repositories. |
| Backlog and acceptance criteria | `docs/backlog.md`, `docs/mvp_scope.md`, `docs/refactor_backlog.md` | Done | Backlog uses release-oriented work items and acceptance-focused tracking. |
| Architecture and Mermaid diagrams | `docs/architecture.md` | Done | Diagrams describe layered architecture and request flows. |
| Technical decisions | `docs/decisions.md` | Done | Documents framework, persistence, repository, and provider decisions. |
| Prompt traceability | `docs/prompts.md` | Done | Sanitized lifecycle prompts support academic reproducibility. |
| Release checklist | `docs/release_checklist.md` | Done | Final submission checks are captured in one place. |
| API examples | `docs/api_examples.md` | Done | Detailed request/response examples are kept outside the README. |
| Responsible AI-assisted development | `README.md`, `docs/prompts.md` | Done | AI supported planning, implementation support, review, tests, and docs; human review remained decisive. |
| Runtime external LLM providers | `docs/external_provider_plan.md`, `docs/local_llm_setup.md` | Out of scope | External providers are future-only planning; current runtime remains local and deterministic. |
| Credentials and paid provider dependency | `.env.example`, `docs/information_governance.md`, `docs/security_checks.md` | Guarded | No provider credentials are required, configured, or needed for tests. |
| Submission quality checks | `scripts/safety_check.py`, `docs/security_checks.md`, `tests/` | Guarded | Tests and safety checks are expected before publication or packaging. |
| Tracked local artifacts | `.gitignore`, `scripts/safety_policy.json` | Guarded | `.env`, databases, caches, ZIP files, and private-path artifacts are blocked or checked. |
| Final release tag | Git history | Deferred | No final tag is created until explicitly requested. |
