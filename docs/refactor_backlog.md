# Refactor Backlog

This backlog is public, post-course maintenance guidance for
`micro-api-work-items`. It is not required to understand or run the current
MVP, and it does not expand the release scope.

The current submission remains:

- public and educational;
- local SQLite only;
- deterministic and provider-free at runtime;
- focused on `/health`, `/work-items`, and `/work-items/classify`;
- covered by automated tests and the deterministic safety checker.

Speculative product, platform, governance, or automation ideas should move to
separate planning after the course submission. They are not part of this public
MVP release.

## Current Architecture

| Layer | Location | Purpose |
| --- | --- | --- |
| Controllers | `app/controllers/` | FastAPI route handlers and HTTP concerns. |
| Schemas | `app/schemas/` | Pydantic request and response contracts. |
| Services | `app/services/` | Application orchestration for CRUD and suggestions. |
| Repositories | `app/repositories/` | SQLAlchemy persistence access. |
| Models | `app/models/` | SQLAlchemy database model. |
| Database | `app/db/database.py` | Engine, session, schema initialization, and SQLite directory handling. |
| Providers | `app/providers/priority/local_provider.py` | Local deterministic PriorityAdvisor rules. |
| Tests | `tests/` | API, service, repository, provider, PriorityAdvisor, and safety-check tests. |

The public API must remain unchanged unless a future task explicitly approves
an API change:

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Health check. |
| `POST` | `/work-items` | Create a work item. |
| `GET` | `/work-items` | List work items. |
| `GET` | `/work-items/{id}` | Retrieve one work item. |
| `PATCH` | `/work-items/{id}` | Partially update one work item. |
| `DELETE` | `/work-items/{id}` | Delete one work item. |
| `POST` | `/work-items/classify` | Suggest type, priority, and tags without persistence. |

## Completed Refactor Work

| ID | Item | Status | Evidence |
| --- | --- | --- | --- |
| REF-001 | Align route modules with controller terminology | Done | `app/controllers/`, `app/main.py` |
| REF-002 | Move persistence model into models layer | Done | `app/models/work_item_model.py` |
| REF-003 | Add repository layer | Done | `app/repositories/work_item_repository.py` |
| REF-004 | Add repository-focused tests | Done | `tests/test_work_item_repository.py` |
| REF-005 | Rename classifier concept to PriorityAdvisor | Done | `app/services/priority_advisor.py` |
| REF-006 | Add local deterministic provider boundary | Done | `app/providers/priority/local_provider.py` |
| REF-007 | Document optional local-provider experimentation as future-only | Done | `docs/local_llm_setup.md` |
| REF-008 | Document optional external-provider planning as future-only | Done | `docs/external_provider_plan.md` |

## Post-Course Maintenance Backlog

| ID | Item | Why it may help later | Stop rule |
| --- | --- | --- | --- |
| REF-009 | Rename `app/services/work_items.py` to `work_item_service.py` | Improves naming consistency with singular domain language. | Do only if imports remain behavior-preserving and tests pass. |
| REF-010 | Add pagination or simple filters | Makes list behavior more realistic for larger local data sets. | Do not add until current MVP is submitted and API change is approved. |
| REF-011 | Add Alembic migrations | Helps if schema evolution becomes necessary. | Do not add for the current SQLite course MVP. |
| REF-012 | Improve tag and metadata validation | Tightens input quality after basic CRUD is accepted. | Keep response shape stable unless separately approved. |
| REF-013 | Revisit identifier strategy | UUIDs may be useful for distributed or public multi-system integration. | Do not replace integer IDs unless external identifier semantics are required. |
| REF-014 | Revisit optional provider experimentation | Could support future comparison with deterministic suggestions. | Keep current runtime local and deterministic; require separate approval before code, dependencies, credentials, or network calls. |

## Provider Boundary

The provider boundary currently exists only to keep deterministic
PriorityAdvisor rules separate from service orchestration. It should not be
read as evidence that external providers are part of the current release.

Current rule:

```text
PriorityAdvisor service -> local deterministic provider -> suggestions only
```

Any future provider experiment must preserve these constraints:

- optional behavior only;
- no CRUD dependency on provider availability;
- no committed credentials;
- no real network calls in tests;
- schema validation before using provider output;
- deterministic local fallback remains available.

## Test Strategy

Use automated regression tests, not a claim of formal test-first TDD, as the
quality evidence for this repository.

Expected checks after any refactor:

```powershell
& 'C:\Users\<your-user>\anaconda3\python.exe' -m pytest -q
& 'C:\Users\<your-user>\anaconda3\python.exe' scripts\safety_check.py
```

Minimum expectations:

- API tests preserve public routes, status codes, and response shape.
- Service tests preserve application behavior.
- Repository tests preserve persistence behavior.
- PriorityAdvisor and provider tests preserve deterministic suggestions.
- Safety-check tests preserve public/private boundary behavior.
- No dependency, schema, route, or database change is bundled into a docs-only
  or naming-only refactor.

## Documentation Update Rules

- Update `README.md` only when setup, scope, verification, or documentation map
  details change.
- Update `docs/architecture.md` when layer boundaries or diagrams change.
- Update `docs/decisions.md` when a meaningful technical decision changes.
- Update `docs/mvp_scope.md` only when MVP boundaries change.
- Update `docs/api_examples.md` only when public request or response examples
  change.

## Current Stop Point

For the course submission, stop here: the completed refactors already support a
clean layered MVP. Further work should wait until after public tagging and
course submission unless it is required to fix a blocker found during release
verification.
