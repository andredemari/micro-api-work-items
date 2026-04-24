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
| P-001 | Planning | CO-STAR, scope control | Define the MVP scope, architecture, exclusions, tests, docs, and commit sequence. | MVP plan and acceptance checklist. | `docs/mvp_scope.md`, `docs/architecture.md` | `docs: define mvp scope and architecture plan` |
| P-002 | Implementation | Incremental implementation, Conventional Commits | Build the FastAPI app, SQLite persistence, CRUD routes, and local classifier. | Application source code and commit sequence. | `app/`, `requirements.txt`, `Makefile` | `feat: add work item schemas services and CRUD routes` |
| P-003 | Testing | Acceptance criteria, regression checks | Create automated coverage for health, CRUD, validation, metadata, tags, timestamps, and deterministic classification. | Pytest suite. | `tests/` | `test: add health CRUD and classifier coverage` |
| P-004 | Documentation | CO-STAR, public-safe writing | Produce setup, run, API, architecture, decisions, and prompt documentation. | README and supporting docs. | `README.md`, `docs/` | `docs: complete README and supporting documentation` |
| P-005 | Review | Checklist-based review | Validate scope limits, local-only classifier behavior, tests, docs, and public-safe constraints. | Final verification notes and README refinements. | `README.md`, `docs/mvp_scope.md` | `docs: improve local environment and API usage instructions` |
| P-006 | Final Hardening | Traceability, academic submission review | Add academic context, license, diagrams, decision rationale, prompt traceability, and local data organization. | Final academic submission hardening updates. | `LICENSE`, `README.md`, `docs/`, `data/` | `docs: add academic context and license`; `docs: add architecture diagrams and technical decisions`; `docs: improve prompt traceability`; `chore: move local sqlite data into data directory` |

## Sanitized Prompt Examples

### P-001 Planning

Context:
You are helping plan `micro-api-work-items`, a small academic FastAPI REST API for managing generic work items.

Objective:
Create an MVP plan with architecture, API behavior, tests, documentation, out-of-scope items, and Conventional Commit sequence.

Style:
Keep the plan concise and implementation-ready.

Tone:
Practical and educational.

Audience:
Students and reviewers evaluating an introductory software engineering mini-project.

Response format:
Use sections for project understanding, architecture, file tree, MVP features, tests, documentation, commits, and risks.

### P-002 Implementation

Context:
The project is a local-first FastAPI backend using Python, Pydantic, SQLAlchemy, SQLite, Uvicorn, and Pytest.

Objective:
Implement health check, CRUD endpoints under `/work-items`, local SQLite persistence, automated tests, and a side-effect-free classifier at `POST /work-items/classify`.

Style:
Use a small layered structure with routes, schemas, database models, services, tests, and documentation.

Tone:
Concise and instructional.

Audience:
Students and reviewers evaluating backend engineering practices.

Response format:
Provide implementation steps, files to create or update, test expectations, and Conventional Commit messages.

### P-003 Testing

Context:
The project has REST endpoints, local SQLite persistence, and deterministic classification rules.

Objective:
Test health, CRUD, validation errors, missing item `404`, tags and metadata persistence, timestamp updates, deterministic classification, and classifier non-persistence.

Style:
Use focused Pytest tests with isolated database setup.

Tone:
Precise and verification-oriented.

Audience:
Developers and academic reviewers.

Response format:
List scenarios and implement readable test functions.

### P-004 Documentation

Context:
The project is an academic backend MVP named `micro-api-work-items`.

Objective:
Document objective, stack, setup, run instructions, API examples, tests, limitations, next steps, architecture, decisions, and prompt usage.

Style:
Keep the writing concise, beginner-friendly, and public-safe.

Tone:
Clear and instructional.

Audience:
Students, instructors, and reviewers.

Response format:
Create README content and supporting Markdown docs.

### P-005 Review

Context:
The implementation is complete and should be checked against the accepted MVP scope.

Objective:
Review code, tests, docs, commit history, runtime constraints, and public-safety requirements.

Style:
Use checklist-based verification.

Tone:
Direct and practical.

Audience:
Project maintainers and reviewers.

Response format:
Report findings, test results, commit log, run command, example requests, and remaining limitations.

### P-006 Final Hardening

Context:
The repository is a small academic FastAPI API prepared for final submission.

Objective:
Improve academic context, license, architecture diagrams, technical decisions, prompt traceability, local data organization, and final verification without expanding product scope.

Style:
Keep changes small, traceable, public-safe, and suitable for an introductory software engineering assignment.

Tone:
Professional and academic.

Audience:
Course reviewers and future students reading the repository.

Response format:
Use small Conventional Commits and report files changed, tests, commit log, artifact tracking checks, and remaining limitations.

## Privacy And Scope Rules

- Do not include raw private chat history.
- Do not include private business context, private paths, credentials, tokens, internal systems, or domain-specific examples.
- Keep prompts generic and reproducible.
- Keep runtime behavior local-first and deterministic.
- Do not introduce external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, frontend, authentication, external integrations, or `python-dotenv`.
