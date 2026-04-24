# Refactor Backlog

## Purpose

This document captures an incremental, public-safe refactor roadmap for `micro-api-work-items`.

The project is already a working academic FastAPI MVP. The goal of this roadmap is not to expand product scope immediately. The goal is to align the internal architecture more closely with the course layered architecture while preserving the current public API and deterministic local runtime behavior.

## Current Architecture Summary

The current application is organized as a small FastAPI backend:

- `app/api/routes/` contains FastAPI route handlers.
- `app/schemas/` contains Pydantic request and response schemas.
- `app/db/models.py` contains the SQLAlchemy persistence model.
- `app/db/database.py` contains database engine, session, and schema initialization.
- `app/services/work_items.py` contains CRUD service logic.
- `app/services/classifier.py` contains deterministic local classification rules.
- `tests/` contains API, service, and classifier tests.

The current public API must remain unchanged:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/work-items` | Create work item |
| `GET` | `/work-items` | List work items |
| `GET` | `/work-items/{id}` | Retrieve one work item |
| `PATCH` | `/work-items/{id}` | Partially update one work item |
| `DELETE` | `/work-items/{id}` | Delete one work item |
| `POST` | `/work-items/classify` | Suggest type, priority, and tags without persistence |

## Target Architecture

The target direction is a layered architecture aligned with the course vocabulary:

```text
Client
  -> Controller/API
    -> Pydantic schemas
    -> Service
      -> Repository
        -> SQLAlchemy model
        -> Database/session
      -> PriorityAdvisor
        -> Local deterministic provider
        -> Future optional providers
```

Near-term target folder direction:

```text
app/
  main.py
  controllers/
    health_controller.py
    work_item_controller.py
  db/
    database.py
  models/
    work_item_model.py
  schemas/
    work_items.py
  repositories/
    work_item_repository.py
  services/
    work_item_service.py
    priority_advisor.py
  providers/
    priority/
      local_provider.py
```

Future-only optional provider direction:

```text
app/
  providers/
    priority/
      ollama_provider.py
      external_provider.py
```

The future-only provider files above must not be created during the immediate refactor. They are planning placeholders for later, separately approved work. The near-term provider architecture should focus on local deterministic behavior.

This is a roadmap, not a single implementation task. Each layer should be introduced in a small, behavior-preserving commit.

## Pydantic Schemas Vs SQLAlchemy Models

The project must preserve a clear distinction between API contracts and persistence models:

- `app/schemas/` contains Pydantic models used for request validation, response serialization, and OpenAPI documentation.
- `app/models/` should contain SQLAlchemy ORM models used to map Python classes to database tables.
- Pydantic schemas should not become database models.
- SQLAlchemy models should not become public API contracts.

This distinction is important because the course may use the term "model" broadly, while this FastAPI project benefits from separating API schemas from database models.

## Current-To-Target Folder Mapping

| Current location | Target location | Purpose | Migration note |
| --- | --- | --- | --- |
| `app/api/routes/health.py` | `app/controllers/health_controller.py` | Health endpoint controller | Preserve `GET /health`. |
| `app/api/routes/work_items.py` | `app/controllers/work_item_controller.py` | Work item API controller | Preserve all `/work-items` routes. |
| `app/db/models.py` | `app/models/work_item_model.py` | SQLAlchemy persistence model | Preserve table and column behavior. |
| `app/db/database.py` | `app/db/database.py` | Engine/session/schema setup | Keep location unless a later refactor requires otherwise. |
| `app/schemas/work_items.py` | `app/schemas/work_items.py` | Pydantic API contracts | Keep location and public schema behavior. |
| `app/services/work_items.py` | `app/services/work_item_service.py` | Work item service orchestration | Rename only when low risk. |
| none | `app/repositories/work_item_repository.py` | Persistence access isolation | Add without changing API behavior. |
| `app/services/classifier.py` | `app/services/priority_advisor.py` | PriorityAdvisor orchestration | Preserve current classifier output. |
| none | `app/providers/priority/local_provider.py` | Deterministic local fallback | Default provider must remain local. |
| none | future-only optional provider modules | Optional LLM provider adapters | Do not create until separately approved. |

## Refactor Roadmap

### Phase 0: Planning Baseline

Create this roadmap and keep it public-safe.

Acceptance criteria:

- `docs/refactor_backlog.md` exists.
- The roadmap preserves the current public API.
- The roadmap clearly separates near-term refactors from future features.
- No application behavior changes.

### Phase 1: Controller And Model Naming Alignment

Align folders with course terminology while preserving behavior.

Planned changes:

- Move API route modules toward `app/controllers/`.
- Move SQLAlchemy model toward `app/models/work_item_model.py`.
- Keep Pydantic schemas in `app/schemas/`.
- Update imports only.
- Keep all routes, status codes, response shapes, and tests unchanged.

Phase 1 describes the conceptual course-aligned structure. It does not require all folder moves to happen before lower-risk coupling reductions such as repository extraction.

### Phase 2: Repository Layer

Introduce a repository layer to isolate persistence operations.

Repository responsibilities:

- create a work item;
- list work items;
- get a work item by id;
- update a work item;
- delete a work item.

The service layer should orchestrate application behavior and call the repository instead of directly owning SQLAlchemy query details.

### Phase 3: PriorityAdvisor Local Refactor

Refactor the current classifier concept into a course-aligned `PriorityAdvisor`.

Requirements:

- preserve `POST /work-items/classify`;
- preserve the current response shape unless separately approved;
- preserve local deterministic behavior;
- keep classifier/advisor flow separate from persisted CRUD flow;
- do not make LLM calls.

### Phase 4: Local Provider Interface

Prepare a provider architecture without requiring external services.

Requirements:

- define a small provider contract for suggestions;
- keep a deterministic local provider as the default;
- optionally add a mock provider for tests;
- do not add network calls;
- do not require credentials.

Near-term provider work should stop at local deterministic behavior. Ollama and external LLM providers are future-only.

### Phase 5: Optional Future LLM Providers

Plan optional providers only after the local provider interface is stable.

Potential future providers:

- local Ollama provider;
- optional external provider.

Constraints:

- LLM providers must be optional.
- Missing provider configuration must not break CRUD.
- Local deterministic fallback must remain available.
- Provider output must be validated before use.
- No credentials may be hardcoded or committed.
- No model files may be stored in the repository.
- Any future external provider must be approved in a separate implementation plan.

### Phase 6: Future Capture And Suggestion Workflow

Plan future human-in-the-loop workflows without implementing them now.

Conceptual flow:

1. Capture raw input.
2. Generate a suggested work item or suggested update.
3. Store the suggestion as pending review.
4. Human reviewer approves, edits, or rejects.
5. Only approved suggestions create or update persisted work items.

### Phase 7: Future Human Review And Audit Trail

Plan review records for suggested changes.

Potential concepts:

- reviewer action;
- approval/edit/rejection;
- reason;
- timestamp;
- suggestion version.

Do not implement database tables until separately approved.

### Phase 8: Future Telemetry

Plan operational traceability for future advisor/provider runs.

Potential event types:

- `priority_advisor.started`;
- `priority_advisor.completed`;
- `priority_advisor.failed`;
- `suggestion.created`;
- `suggestion.approved`;
- `suggestion.rejected`;
- `work_item.status_changed`.

Telemetry should remain generic and must not record credentials or private data.

### Phase 9: Future Controlled Autonomy

Controlled autonomy must remain future-only.

Possible levels:

| Level | Meaning |
| --- | --- |
| 0 | AI disabled |
| 1 | AI suggests only |
| 2 | AI drafts and human approves |
| 3 | AI applies low-risk changes and human audits later |
| 4 | AI acts within bounded routines |

Near-term planning should stay at Level 1 or Level 2.

## Backlog

| ID | Phase | Item | Rationale | Likely files affected | Tests | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REF-000 | 0 | Create refactor roadmap | Establish public-safe incremental plan | `docs/refactor_backlog.md` | Not required | Roadmap exists; no app behavior changes | Done |
| REF-001 | 1 | Move route modules to controllers | Align with course Controller terminology | `app/controllers/*`, `app/main.py`, imports | Full suite | Public routes unchanged; tests pass | Planned |
| REF-002 | 1 | Move SQLAlchemy model to models layer | Separate database models from database setup | `app/models/work_item_model.py`, imports | Full suite | Table behavior unchanged; tests pass | Planned |
| REF-003 | 2 | Add work item repository | Isolate SQLAlchemy persistence operations | `app/repositories/work_item_repository.py`, service imports | Repository/service/API tests | Service uses repository; API unchanged | Done |
| REF-004 | 2 | Add repository-focused tests | Improve diagnosis of persistence behavior | `tests/` | Full suite | Repository CRUD behavior covered | Done |
| REF-005 | 3 | Refactor classifier to PriorityAdvisor | Align with course PriorityAdvisor concept | `app/services/priority_advisor.py`, imports | Classifier/advisor tests | Current suggestions preserved | Planned |
| REF-006 | 4 | Add local provider interface | Prepare optional providers safely | `app/providers/priority/local_provider.py` | Provider tests | Local deterministic provider remains default | Future |
| REF-007 | 5 | Plan optional Ollama provider | Support local experimentation later | docs first, later future provider module | Mocked tests only | Missing local provider does not break app | Future |
| REF-008 | 5 | Plan optional external provider | Support explicitly configured provider later | docs first, later future provider module | Mocked tests only | No credentials required by default | Future |
| REF-009 | 6 | Plan capture concept | Support future raw-input workflow | docs first | Not required | Capture design documented only | Future |
| REF-010 | 6 | Plan pending suggestions | Support human review before applying changes | docs first | Not required | Suggestion lifecycle documented only | Future |
| REF-011 | 7 | Plan human review records | Keep human approval explicit | docs first | Not required | Review model described, not implemented | Future |
| REF-012 | 8 | Plan telemetry taxonomy | Improve future traceability | docs first | Not required | Generic event list documented | Future |
| REF-013 | 9 | Plan controlled autonomy policy | Prevent unsafe expansion | docs first | Not required | Autonomy limits documented | Future |
| REF-014 | 9 | Plan agent-ready context | Define future agent rules and policies | docs first | Not required | `.agent/` purpose documented only | Future |

## Explicit Out Of Scope

Do not implement as part of this planning document:

- new public endpoints;
- route changes;
- response format changes;
- schema behavior changes;
- new database tables;
- LLM providers;
- autonomous agents;
- script execution;
- sandbox orchestration;
- multi-tenant runtime isolation;
- web browsing;
- external integrations;
- authentication;
- frontend;
- Docker;
- CI/CD;
- `.agent/` folder creation;
- tag or release creation.

## Future Runtime Security Constraints

If script execution, tool execution, or autonomous agent runtimes are ever considered, they must be planned as a separate execution subsystem.

Security constraints:

- Do not execute untrusted code in the API process.
- Treat agent/tool/script workloads as untrusted.
- Use isolated workers or sandboxes before any execution capability exists.
- Apply CPU, memory, process, filesystem, and network limits.
- Deny network access by default unless explicitly required.
- Never mount broad host paths into execution environments.
- Never expose secrets broadly to runtime workers.
- Record telemetry and audit events for every execution.
- Keep workspaces ephemeral.
- Keep execution outputs size-limited.
- Require human review for risky actions.

These constraints are future planning notes only. The current MVP must not implement script execution or sandbox orchestration.

## Future Agent-Ready Context

A future `.agent/` folder may be planned later to document agent-facing rules, prompts, policies, safe operating boundaries, and expected agent behavior.

The `.agent/` folder must not be created in this planning step. Any future agent-ready context should remain public-safe, generic, and separate from private strategy, credentials, internal systems, or domain-specific operational details.

## Documentation Update Strategy

Update documentation with each refactor phase:

- `README.md`: only if setup, architecture summary, or docs map changes.
- `docs/architecture.md`: update diagrams and course terminology mapping after folder/layer changes.
- `docs/decisions.md`: record new architectural decisions such as repository introduction.
- `docs/mvp_scope.md`: keep public API and MVP boundaries clear.
- `docs/prompts.md`: add sanitized prompt traceability for each significant planning or refactor step.
- `docs/api_examples.md`: update only if public API examples change, which is not expected for behavior-preserving refactors.

## Test Strategy

Run the full suite after every refactor phase:

```powershell
& 'C:\Users\<your-user>\anaconda3\python.exe' -m pytest -q
```

Minimum expectations:

- API tests continue to prove public routes and response behavior.
- Service tests continue to prove business behavior.
- Repository tests should be added when the repository layer is introduced.
- PriorityAdvisor tests must preserve current deterministic classifier behavior.
- Provider tests must use mocks or local deterministic logic only unless a future provider implementation is separately approved.
- No real external network calls should be required for tests.

## Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Public API changes accidentally | Keep existing API tests unchanged and passing. |
| Import churn during folder moves | Move one layer at a time and run tests after each commit. |
| Pydantic schemas and SQLAlchemy models becoming confused | Keep `app/schemas/` and `app/models/` separate. |
| Repository layer adding noise | Keep repository small and focused on persistence operations. |
| PriorityAdvisor refactor changing classifier output | Preserve current classifier tests and add advisor-level regression tests. |
| Optional providers making runtime brittle | Keep local deterministic fallback mandatory and providers optional. |
| Credentials leaking into public repo | Do not hardcode secrets; do not commit local env files. |
| Scope expanding into agents or automation | Keep future concepts documented but unimplemented until separately approved. |
| Runtime execution creating security exposure | Do not implement script execution in the MVP; require a separate security design first. |

## Suggested Conventional Commit Sequence

```text
docs: add refactor backlog roadmap
refactor: add repository layer for work items
test: add repository coverage
refactor: align controllers with course architecture
refactor: move persistence model into models layer
refactor: rename classifier to priority advisor
refactor: add local priority provider interface
docs: update architecture after refactor phases
```

Each implementation commit should be small and behavior-preserving unless a future change is explicitly approved.

## Recommended First Implementation Task After Planning

After this planning document is committed, the safest first implementation task is:

```text
refactor: add repository layer for work items
```

Reason:

- It improves layering without changing public routes.
- It keeps folder renaming churn lower than a full controller/model move.
- It reduces coupling before broader folder moves.
- It can be verified with existing service/API tests plus small repository tests.
- It prepares the service layer for later PriorityAdvisor and provider refactors.
