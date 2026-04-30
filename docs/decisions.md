# Decisions

This file is a lightweight ADR-style decision log for the academic MVP. Each
entry records the context, decision, rationale, consequences, and current
status without splitting the small project into many separate ADR files.

## ADR-001: Keep The MVP Local And Course-Oriented

- Status: Accepted.
- Context: The project implements a small "Micro-API de Tarefas" style backend
  for course review and reproducible local execution.
- Decision: Keep the current release public, academic, deterministic, local,
  and simple.
- Rationale: A narrow scope is easier to inspect, run, test, and submit. It
  also avoids confusing the reviewer with infrastructure that is not required
  by the course task.
- Consequences: Authentication, frontend, Docker, CI/CD, external integrations,
  runtime AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming,
  and deployment automation are out of scope for this release.

## ADR-002: FastAPI, Pydantic V2, SQLAlchemy, And SQLite

- Status: Accepted.
- Context: The API needs explicit request validation, clear routes, local
  persistence, and straightforward automated tests.
- Decision: Use FastAPI for HTTP routing and OpenAPI support, Pydantic v2 for
  request and response contracts, SQLAlchemy for persistence, and SQLite for
  the local database.
- Rationale: This stack demonstrates the backend concepts with little
  boilerplate and no external service dependency. Flask would also be valid,
  but FastAPI reduces manual validation and documentation work.
- Consequences: The app runs locally with `sqlite:///./data/work_items.db` by
  default. SQLite is sufficient for the course MVP, but production deployment
  would require a separate persistence decision.

## ADR-003: Layered Organization For Maintainability

- Status: Accepted.
- Context: The course vocabulary references controllers, models, services, and
  persistence. The implementation should be easy to review without overbuilding.
- Decision: Organize the code into controllers, schemas, services,
  repositories, SQLAlchemy models, database setup, and providers.
- Rationale: Controllers own HTTP concerns, schemas define the API contract,
  services orchestrate behavior, repositories isolate SQLAlchemy access, models
  map persisted data, and providers isolate suggestion logic.
- Consequences: The public API remains small while the code has clear
  maintenance boundaries. The repository layer is intentionally small and does
  not change routes, schemas, response formats, database tables, or runtime
  behavior.

## ADR-004: Separate Pydantic Schemas From SQLAlchemy Models

- Status: Accepted.
- Context: The word "model" can mean both API contract and persistence model.
- Decision: Keep Pydantic API contracts in `app/schemas/` and SQLAlchemy ORM
  models in `app/models/`.
- Rationale: API validation and database mapping evolve for different reasons.
  Keeping them separate makes changes easier to review and test.
- Consequences: The API exposes `metadata`, while the SQLAlchemy model uses the
  internal attribute `metadata_json` because SQLAlchemy reserves `metadata` on
  declarative models. The database column is still named `metadata`.

## ADR-005: Use PATCH For Partial Updates

- Status: Accepted.
- Context: The course task requires updating status or priority. The API only
  needs partial updates.
- Decision: Implement `PATCH /work-items/{id}` and do not add `PUT`.
- Rationale: `PATCH` matches the current update behavior because clients can
  send only the fields they want to change.
- Consequences: The endpoint set stays smaller, and tests focus on partial
  update behavior.

## ADR-006: Use Integer IDs For The Local SQLite MVP

- Status: Accepted.
- Context: Work items are stored in a single local SQLite database for a course
  project. The API is not a distributed public integration surface.
- Decision: Use simple integer primary keys for persisted work items.
- Rationale: Integer IDs are easy to inspect in examples, curl commands, tests,
  and short presentations. They are enough for one local database and avoid
  adding identifier complexity before it is needed.
- Consequences: UUIDs are not implemented in this release. UUIDs may be
  reconsidered later if the API needs distributed ID generation, public
  multi-system integration, or stronger external identifier semantics.

## ADR-007: Keep Classification Side-Effect Free

- Status: Accepted.
- Context: The course includes a priority or classification suggestion idea, but
  the CRUD API must remain predictable.
- Decision: Implement `POST /work-items/classify` as a side-effect-free
  suggestion endpoint.
- Rationale: The endpoint can demonstrate classification behavior without
  creating, updating, deleting, or reading persisted work items.
- Consequences: Classification responses are suggestions only. Persisted CRUD
  behavior remains separate and deterministic.

## ADR-008: PriorityAdvisor Means Local Deterministic Suggestions

- Status: Accepted.
- Context: `PriorityAdvisor` is course-aligned terminology that could be
  mistaken for an external AI provider.
- Decision: In this project, `PriorityAdvisor` means the local deterministic
  implementation of the course priority/classification suggestion idea.
- Rationale: The name keeps the course concept visible while the implementation
  remains simple: keyword rules produce suggested type, priority, tags, and
  reasons through `app/providers/priority/local_provider.py`.
- Consequences: `PriorityAdvisor` is not an external AI provider, does not call
  an LLM, does not require credentials, and does not persist data.

## ADR-009: Defer Runtime AI Provider Integration

- Status: Accepted.
- Context: Optional local or external AI providers are future ideas, not
  requirements for the course MVP.
- Decision: Do not add runtime provider selection, provider registries,
  credentials, network calls, model downloads, dependencies, or environment
  variables in this release.
- Rationale: Provider integration would add operational and privacy concerns
  that are not necessary for demonstrating the micro-API.
- Consequences: Any future provider work must be separately approved, optional,
  mock-tested, bounded by timeouts, validated against the existing response
  schema, and backed by the deterministic local fallback.

## ADR-010: Keep Environment Configuration Minimal

- Status: Accepted.
- Context: The app only needs a database URL override for local experimentation.
- Decision: Read environment variables from the operating system and keep
  `.env.example` as reference documentation only.
- Rationale: Avoiding `python-dotenv` keeps dependencies and runtime behavior
  simple.
- Consequences: No provider credentials or LLM settings are needed. If
  `DATABASE_URL` is not set, the app defaults to local SQLite.

## ADR-011: Use Automated And Regression Tests

- Status: Accepted.
- Context: The repository includes tests for API, service, repository,
  PriorityAdvisor, provider, and safety-check behavior.
- Decision: Describe the workflow as automated tests, regression tests,
  test-supported development, and safety-check tests.
- Rationale: The Git history supports tested development and regression
  coverage, but it should not claim formal test-first TDD unless the evidence
  shows a strict red/green/refactor sequence.
- Consequences: Documentation should avoid overstating TDD and should focus on
  the actual verification evidence.
