# MVP Scope

## Goal

Build a small public REST API for managing generic work items with local SQLite persistence, automated tests, documentation, and a deterministic local classifier.

## In Scope

- Health check endpoint.
- CRUD endpoints under `/work-items`.
- Partial updates with `PATCH /work-items/{id}`.
- Local SQLite persistence.
- Pydantic v2 validation.
- SQLAlchemy data model.
- Side-effect-free classifier at `POST /work-items/classify`.
- Automated tests with Pytest.
- Project documentation.
- Conventional Commit history.

## Out Of Scope

- External AI providers.
- LLM APIs.
- Embeddings.
- RAG.
- Agents.
- Queues.
- Streaming.
- Frontend.
- Authentication.
- External integrations.
- `python-dotenv`.

## Acceptance Checklist

Use this checklist as a project validation reference.

### Git And Commit History Requirements

- [ ] The project initializes a Git repository before implementation.
- [ ] The project uses meaningful Conventional Commits.
- [ ] The commit history follows the approved implementation sequence unless a small technical adjustment is necessary.
- [ ] No implementation files are created before Git initialization.
- [ ] Tests are run before the final documentation commit.

### Project Structure Requirements

- [ ] The project is named `micro-api-work-items`.
- [ ] The backend source code is organized under `app/`.
- [ ] API routes are separated from schemas, database code, and services.
- [ ] Tests are organized under `tests/`.
- [ ] Supporting documentation is organized under `docs/`.
- [ ] The project includes `README.md`, `requirements.txt`, `Makefile`, `.gitignore`, and `.env.example`.

### API Behavior Requirements

- [ ] `GET /health` returns a successful response.
- [ ] `POST /work-items` creates and persists a work item.
- [ ] `GET /work-items` lists persisted work items.
- [ ] `GET /work-items/{id}` returns a persisted work item by id.
- [ ] `PATCH /work-items/{id}` partially updates a persisted work item.
- [ ] `DELETE /work-items/{id}` deletes a persisted work item.
- [ ] `POST /work-items/classify` returns suggestions without persisting data.
- [ ] Missing work items return `404`.
- [ ] Invalid enum values return validation errors.

### Data Model Requirements

- [ ] A work item includes `id`, `title`, `description`, `status`, `priority`, `type`, `source`, `tags`, `metadata`, `created_at`, and `updated_at`.
- [ ] `status` supports only `open`, `in_progress`, `done`, and `archived`.
- [ ] `priority` supports only `low`, `medium`, `high`, and `critical`.
- [ ] `type` supports only `task`, `bug`, `improvement`, `research`, `operation`, and `incident`.
- [ ] `source` supports only `manual`, `system`, and `other`.
- [ ] `tags` are persisted as a list of strings.
- [ ] `metadata` is persisted as an optional JSON field.
- [ ] `created_at` is set by the backend.
- [ ] `updated_at` changes after partial updates.
- [ ] SQLAlchemy does not expose a model attribute named `metadata` that conflicts with declarative metadata.

### Local Classifier Requirements

- [ ] The classifier uses only local deterministic rules.
- [ ] The classifier does not use external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, or external integrations.
- [ ] The classifier receives input data and returns suggestions.
- [ ] The classifier does not persist data.
- [ ] The persisted CRUD flow remains separate from the classifier flow.
- [ ] The same classifier input returns the same classifier output.

### Test Coverage Requirements

- [ ] Tests cover the health endpoint.
- [ ] Tests cover creating a work item.
- [ ] Tests cover listing work items.
- [ ] Tests cover retrieving a work item by id.
- [ ] Tests cover partial updates with `PATCH`.
- [ ] Tests cover deleting a work item.
- [ ] Tests cover validation errors for invalid enum values.
- [ ] Tests cover missing item `404` responses.
- [ ] Tests cover tags persistence.
- [ ] Tests cover metadata persistence.
- [ ] Tests cover `updated_at` behavior.
- [ ] Tests cover deterministic classification.
- [ ] Tests verify classification does not persist data.

### Documentation Requirements

- [ ] `README.md` explains the project objective.
- [ ] `README.md` explains that a work item is a generic task-like record.
- [ ] `README.md` lists the technology stack.
- [ ] `README.md` includes setup instructions.
- [ ] `README.md` includes run instructions.
- [ ] `README.md` includes API examples with `curl`.
- [ ] `README.md` includes test instructions.
- [ ] `README.md` includes limitations and next steps.
- [ ] `README.md` explains how generative AI supported development.
- [ ] `docs/architecture.md` describes the architecture and request flow.
- [ ] `docs/mvp_scope.md` describes MVP scope and validation criteria.
- [ ] `docs/decisions.md` records key technical decisions.
- [ ] `docs/prompts.md` documents generic CO-STAR prompts for reproducibility.
- [ ] `.env.example` is documented as a reference file only.
- [ ] The project does not use `python-dotenv`.

### Explicit Out-Of-Scope Items

- [ ] The project does not include external AI providers.
- [ ] The project does not include LLM APIs.
- [ ] The project does not include embeddings.
- [ ] The project does not include RAG.
- [ ] The project does not include agents.
- [ ] The project does not include queues.
- [ ] The project does not include streaming.
- [ ] The project does not include a frontend.
- [ ] The project does not include authentication.
- [ ] The project does not include external integrations.
- [ ] The project does not include `python-dotenv`.

### Final Delivery Report Requirements

- [ ] The final report includes the final file tree.
- [ ] The final report includes `git log --oneline`.
- [ ] The final report includes the test command used and result.
- [ ] The final report includes the run command.
- [ ] The final report includes example `curl` requests.
- [ ] The final report includes any remaining limitations.
