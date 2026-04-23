# Prompt Documentation

This document records public, generic prompts used to support academic reproducibility. The prompts are normalized rather than copied as raw transcripts.

## CO-STAR Structure

- Context: background and constraints.
- Objective: what the prompt asks for.
- Style: preferred implementation or writing style.
- Tone: communication style.
- Audience: intended reader or user.
- Response format: expected output shape.

## Prompt Log

| Lifecycle phase | Prompt title | Purpose | Output used |
| --- | --- | --- | --- |
| Planning | MVP planning prompt | Define scope, architecture, API behavior, tests, docs, and commit sequence. | Execution plan and acceptance checklist. |
| Implementation | Backend implementation prompt | Implement the FastAPI app, SQLite persistence, CRUD routes, and local classifier. | Application source code. |
| Testing | Test coverage prompt | Check required behavior and deterministic classification. | Pytest suite. |
| Documentation | Documentation prompt | Produce README and supporting docs. | README and `docs/` files. |
| Review | Final review prompt | Validate implementation against scope and constraints. | Final verification and delivery report. |

## Generic Prompt Rules

- Use only the public project name `micro-api-work-items`.
- Use generic academic wording.
- Exclude private paths, names, credentials, tokens, internal systems, and private business context.
- Avoid domain-specific examples beyond generic work item categories.
- Prefer concise reproducibility prompts over raw chat history.

## Planning Prompt

Context:
You are helping plan `micro-api-work-items`, a small academic FastAPI REST API for managing generic work items.

Objective:
Create a practical MVP plan with architecture, API behavior, test strategy, documentation plan, out-of-scope items, and Conventional Commit sequence.

Style:
Keep the plan concise and implementation-ready.

Tone:
Practical and educational.

Audience:
Students and reviewers evaluating an introductory software engineering mini-project.

Response format:
Use short sections for project understanding, architecture, file tree, MVP features, tests, documentation, commits, and risks.

## Implementation Prompt

Context:
You are helping implement `micro-api-work-items`, a small academic FastAPI REST API for managing generic work items. The project uses Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy, SQLite, Uvicorn, Pytest, and HTTPX if needed. The MVP must remain local and deterministic.

Objective:
Implement a clean backend with health check, CRUD endpoints under `/work-items`, SQLite persistence, Pydantic schemas, SQLAlchemy models, automated tests, and a side-effect-free local rule-based classifier at `POST /work-items/classify`. The classifier must return suggestions only and must not persist data.

Style:
Keep the code simple, readable, and appropriate for an introductory software engineering assignment. Use a small layered structure with routes, schemas, database models, services, tests, and documentation.

Tone:
Practical, concise, and educational.

Audience:
Students and reviewers evaluating a small backend MVP with good engineering practices.

Response format:
Provide implementation steps, files to create or update, test coverage expectations, and Conventional Commit messages. Do not include external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, frontend, authentication, external integrations, or `python-dotenv`.

## Testing Prompt

Context:
The project is a local FastAPI API with SQLite persistence and a deterministic classifier.

Objective:
Create tests for health, CRUD, validation errors, missing item `404`, tags and metadata persistence, `updated_at` behavior, deterministic classification, and classifier non-persistence.

Style:
Use focused Pytest tests with an isolated test database.

Tone:
Precise and verification-oriented.

Audience:
Developers and academic reviewers.

Response format:
List required test scenarios and implement them as readable test functions.

## Documentation Prompt

Context:
The project is an academic backend MVP named `micro-api-work-items`.

Objective:
Document objective, stack, setup, run instructions, API examples, tests, limitations, next steps, architecture, decisions, MVP scope, and prompt usage.

Style:
Keep the writing concise and public-safe.

Tone:
Clear and instructional.

Audience:
Students, instructors, and reviewers.

Response format:
Create README content and supporting Markdown docs.

## Review Prompt

Context:
The project implementation is complete and should be checked against the accepted MVP scope.

Objective:
Review the code, tests, docs, commit history, and runtime constraints.

Style:
Focus on verifiable acceptance criteria.

Tone:
Direct and practical.

Audience:
Project maintainers and reviewers.

Response format:
Report pass/fail status, test results, commit log, run command, example requests, and remaining limitations.
