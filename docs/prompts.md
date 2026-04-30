# Prompt Traceability

This document records sanitized, representative prompts used to support
academic reproducibility. It is not raw chat history. The prompts are written
to show the kind of AI-assisted work used across planning, implementation,
review, documentation, and final hardening.

## Public-Safe Rules

- Do not include private chat history, private paths, credentials, tokens,
  internal systems, customer data, or private strategy.
- Keep examples generic and course-oriented.
- Preserve the current MVP boundary: local, deterministic, public, and simple.
- Do not introduce runtime external AI providers, local LLM runtime behavior,
  embeddings, RAG, agents, queues, streaming, frontend, authentication,
  external integrations, or `python-dotenv`.

## CO-STAR-Like Shape

The prompts below use a compact CO-STAR-like structure:

- Context: background and constraints.
- Objective: what the assistant should produce.
- Style: implementation or writing expectations.
- Tone: how the response should read.
- Audience: who will review or use the result.
- Response: expected output format.

## Traceability Log

| ID | Phase | Main artifacts | Verification evidence |
| --- | --- | --- | --- |
| P-001 | Scope planning | `docs/mvp_scope.md`, `docs/architecture.md` | MVP scope, out-of-scope list, route plan |
| P-002 | Project setup | `.gitignore`, `requirements.txt`, `Makefile`, `.env.example` | Local setup commands and ignored artifacts |
| P-003 | API implementation | `app/main.py`, `app/controllers/`, `app/schemas/`, `app/services/` | Health, CRUD, validation, and error tests |
| P-004 | Persistence | `app/db/database.py`, `app/models/`, `app/repositories/` | Service and repository tests |
| P-005 | PriorityAdvisor | `app/services/priority_advisor.py`, `app/providers/priority/local_provider.py` | Deterministic classifier and provider tests |
| P-006 | Documentation | `README.md`, `docs/api_examples.md`, `docs/decisions.md` | Reproducible setup, examples, decisions |
| P-007 | Review and safety | `scripts/safety_check.py`, `scripts/safety_policy.json`, `tests/test_safety_check.py` | Safety-check tests and release gate |
| P-008 | Final course readiness | `docs/course_submission_traceability.md`, `docs/release_checklist.md` | Requirement-to-artifact mapping |

## Representative Sanitized Prompts

### P-001 Scope Planning

- Context: A postgraduate course requires a small task-oriented micro-API.
  The repository must remain public, academic, local, deterministic, and easy
  to run.
- Objective: Plan a FastAPI MVP for generic work items, including endpoints,
  data fields, architecture, tests, documentation, and explicit exclusions.
- Style: Keep the plan incremental and implementation-ready.
- Tone: Direct and reviewer-friendly.
- Audience: Course reviewer and future maintainer.
- Response: MVP scope, acceptance checklist, file layout, and commit sequence.

### P-002 Project Setup

- Context: The project should run locally without external services or paid
  provider credentials.
- Objective: Define Python dependencies, ignored local artifacts, environment
  reference values, and basic Makefile commands.
- Style: Prefer simple commands and Windows-friendly guidance.
- Tone: Practical.
- Audience: Student, reviewer, and anyone reproducing the project.
- Response: `.gitignore`, `requirements.txt`, `.env.example`, and Makefile
  targets for install, run, test, and safety checks.

### P-003 API Implementation

- Context: The API needs health, CRUD, and classification endpoints under the
  work-item vocabulary.
- Objective: Implement FastAPI routes, Pydantic contracts, service functions,
  and HTTP error handling without expanding scope.
- Style: Keep controllers thin and move application behavior into services.
- Tone: Precise and conservative.
- Audience: Maintainer reviewing the code.
- Response: Route handlers, schemas, services, and tests for success and error
  cases.

### P-004 Persistence

- Context: Persistence should be local and inspectable for the MVP.
- Objective: Configure SQLite through SQLAlchemy, isolate database access, and
  make tests independent from the runtime database file.
- Style: Use a small repository layer rather than spreading queries through
  route functions.
- Tone: Engineering-focused.
- Audience: Course reviewer and future maintainer.
- Response: Database setup, SQLAlchemy model, repository functions, and
  repository/service regression tests.

### P-005 PriorityAdvisor

- Context: The course includes the idea of suggesting priority or
  classification, but the current release must not call an external AI
  provider.
- Objective: Represent `PriorityAdvisor` as local deterministic suggestion
  logic that returns type, priority, tags, and reasons.
- Style: Keep the endpoint side-effect free and keep persisted CRUD separate.
- Tone: Clear about boundaries.
- Audience: Reviewer checking whether AI runtime scope was added.
- Response: Local provider rules, PriorityAdvisor service, classification
  endpoint, and tests proving deterministic non-persistence.

### P-006 Documentation

- Context: The repository is intended for public GitHub publication and course
  submission.
- Objective: Explain objective, setup, run commands, endpoints, examples,
  limitations, AI assistance, design decisions, and packaging guidance.
- Style: Keep README concise and move detailed evidence into supporting docs.
- Tone: Public-safe and course-oriented.
- Audience: Course reviewer and public reader.
- Response: README updates, API examples, decision log, traceability document,
  and release checklist.

### P-007 Review And Safety

- Context: Public publication requires checking tracked files, ignored local
  artifacts, provider scope, and accidental sensitive content.
- Objective: Add deterministic repository checks and tests without deleting
  files, rewriting history, staging files, or using AI inference.
- Style: Prefer explicit policy data, redacted findings, and temporary Git
  repositories in tests.
- Tone: Strict and factual.
- Audience: Maintainer preparing a release.
- Response: Safety checker, policy data, safety-check tests, and documentation
  for pre-publication use.

### P-008 Final Course Readiness

- Context: Before tagging, the project needs a clean course-submission story
  and evidence that the MVP remained within scope.
- Objective: Map course expectations to repository artifacts, clarify final
  limitations, and verify public/private boundaries.
- Style: Use a checklist and concise artifact mapping.
- Tone: Evidence-based.
- Audience: Course reviewer.
- Response: Course traceability, release checklist updates, and a short
  pre-publication review summary.
