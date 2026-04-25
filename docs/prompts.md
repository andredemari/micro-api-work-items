# Prompt Documentation

This document records public, generic prompts used to support academic reproducibility and traceability. The entries are sanitized summaries, not raw private chat history.

## CO-STAR Structure

- Context: background and constraints.
- Objective: what the prompt asks for.
- Style: preferred implementation or writing style.
- Tone: communication style.
- Audience: intended reader or user.
- Response format: expected output shape.

## Traceability Log

| Prompt ID | Lifecycle Phase | Technique | Purpose | Main Output | Related Artifact | Related Commit |
| --- | --- | --- | --- | --- | --- | --- |
| P-001 | Scope/planning | CO-STAR, scope control | Define the MVP scope, route vocabulary, exclusions, architecture, tests, docs, and commit plan. | MVP plan and acceptance checklist. | `docs/mvp_scope.md`, `docs/architecture.md` | `docs: define mvp scope and architecture plan` |
| P-002 | `.gitignore`/setup | Reproducibility checklist | Create local setup files, dependency list, ignored artifacts, and basic Makefile commands. | Project configuration. | `.gitignore`, `requirements.txt`, `Makefile` | `chore: initialize project configuration` |
| P-003 | README | Public-safe documentation | Explain objective, setup, run, test, API usage, limitations, academic context, and license. | Reproducible project overview. | `README.md`, `LICENSE` | `docs: complete README and supporting documentation`; `docs: add academic context and license` |
| P-004 | Healthcheck | Incremental backend implementation | Add a minimal FastAPI application and service health endpoint. | Health route and app entrypoint. | `app/main.py`, `app/controllers/health_controller.py` | `feat: add FastAPI app and health endpoint` |
| P-005 | Models/schemas | Contract-first design | Define work item fields, enum values, request schemas, response schemas, and classifier schemas. | Pydantic API contract and SQLAlchemy model. | `app/schemas/work_items.py`, `app/models/work_item_model.py` | `feat: configure SQLite persistence and work item model`; `feat: add work item schemas services and CRUD routes` |
| P-006 | Service | Layered architecture | Implement CRUD behavior behind route functions without changing HTTP contracts. | Work item service functions. | `app/services/work_items.py` | `feat: add work item schemas services and CRUD routes` |
| P-007 | Persistence | Local-first data design | Configure SQLite persistence, session handling, test isolation, and ignored local database files. | Database configuration and local data organization. | `app/db/database.py`, `data/.gitkeep`, `.env.example` | `feat: configure SQLite persistence and work item model`; `chore: move local sqlite data into data directory` |
| P-008 | Classifier/PriorityAdvisor | Deterministic local rules | Represent the course PriorityAdvisor idea with local rule-based classification and no persistence side effects. | PriorityAdvisor service, local provider, and classifier route. | `app/services/priority_advisor.py`, `app/providers/priority/local_provider.py`, `app/controllers/work_item_controller.py` | `feat: add local rule-based classifier`; `docs: map course task API scope to work items`; `refactor: rename classifier to priority advisor`; `refactor: add local priority provider` |
| P-009 | API routes | REST route implementation | Expose CRUD and classification behavior under `/work-items` using current MVP routes. | API controller module. | `app/controllers/work_item_controller.py` | `feat: add work item schemas services and CRUD routes` |
| P-010 | Tests | Acceptance criteria, regression checks | Cover health, CRUD, validation errors, missing items, timestamps, metadata, tags, and classifier non-persistence. | Pytest suite. | `tests/` | `test: add health CRUD and classifier coverage` |
| P-011 | Review | Checklist-based review | Validate scope limits, local-only runtime behavior, public-safe docs, tracked artifacts, and final course guidance. | Review notes and final hardening tasks. | `docs/mvp_scope.md`, `docs/release_checklist.md` | `docs: add backlog demo and release checklist` |
| P-012 | Final documentation/release | Release readiness | Add backlog, release checklist, prompt traceability, and reproducibility notes. | Final academic submission documentation. | `docs/backlog.md`, `docs/release_checklist.md`, `docs/prompts.md` | `docs: add backlog demo and release checklist`; `docs: expand prompt lifecycle traceability` |
| P-013 | Local LLM planning | Documentation-first future planning | Document optional local Ollama setup guidance while keeping the current MVP deterministic and provider-free at runtime. | Local LLM setup guidance. | `docs/local_llm_setup.md`, `docs/refactor_backlog.md` | `docs: add local llm setup guidance` |
| P-014 | External provider planning | Provider-agnostic future planning | Document optional external provider constraints, safety controls, fallback behavior, and mock-only test strategy without implementing runtime integration. | External provider planning guidance. | `docs/external_provider_plan.md`, `docs/refactor_backlog.md` | `docs: add external provider planning guidance` |
| P-015 | Security governance | Public-safety hardening | Add preventive governance docs and ignore rules for private notes, credentials, local artifacts, and sensitive files. | Security cleanup runbook and information governance guide. | `.gitignore`, `docs/security_cleanup_runbook.md`, `docs/information_governance.md` | `docs: add security governance and cleanup runbook` |

## Compact Sanitized Prompt Examples

### P-001 Scope/Planning

Plan a small academic FastAPI MVP for generic work items. Include scope, out-of-scope items, architecture, API routes, persistence, tests, documentation, and Conventional Commit sequence.

### P-002 `.gitignore`/Setup

Create basic local project configuration for a Python FastAPI MVP. Include dependency list, ignored Python/cache/database artifacts, and simple install/run/test commands.

### P-003 README

Write public-safe README content for an academic micro-API, including objective, setup, run, tests, API examples, limitations, AI-assisted development notes, and license.

### P-004 Healthcheck

Add a minimal FastAPI application with a health endpoint that can be tested automatically and used as the first runtime verification.

### P-005 Models/Schemas

Define Pydantic v2 schemas and SQLAlchemy models for a generic work item with enum-backed fields, tags, optional metadata, and timestamps.

### P-006 Service

Implement work item CRUD service functions with clear type hints while keeping HTTP route handling separate from persistence operations.

### P-007 Persistence

Configure local SQLite persistence for the MVP, keep runtime database files ignored, and isolate tests from runtime data.

### P-008 Classifier/PriorityAdvisor

Represent the course PriorityAdvisor concept with a local deterministic advisor that returns classification suggestions without persisting data or calling external AI providers.

### P-009 API Routes

Expose work item CRUD routes and the classifier route under `/work-items`, using `PATCH` for partial updates and preserving the MVP route contract.

### P-010 Tests

Create automated tests for health, CRUD, validation errors, missing items, tags, metadata, timestamps, deterministic classification, and classifier non-persistence.

### P-011 Review

Review the repository against MVP scope, public-safety constraints, test coverage, documentation completeness, tracked artifacts, and course submission expectations.

### P-012 Final Documentation/Release

Prepare final academic submission documentation with backlog, release checklist, prompt traceability, reproducibility notes, and verification commands.

### P-013 Local LLM Planning

Document optional local LLM setup with Ollama for future experimentation, keeping current runtime behavior unchanged and avoiding provider code, credentials, dependencies, or environment variables.

### P-014 External Provider Planning

Document future optional external provider integration in provider-agnostic terms, requiring credential safety, timeouts, schema validation, local fallback, privacy controls, and mock-only tests before any implementation.

### P-015 Security Governance

Add public-safe governance guidance for accidental sensitive commits, ignored private working areas, information classification, and pre-publication review without changing runtime behavior.

## Privacy And Scope Rules

- Do not include raw private chat history.
- Do not include private business context, private paths, credentials, tokens, internal systems, or domain-specific examples.
- Keep prompts generic and reproducible.
- Keep runtime behavior local-first and deterministic.
- Do not introduce external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, frontend, authentication, external integrations, or `python-dotenv`.
