# Release Checklist

Use this checklist before submitting the academic MVP.

## Scope

- [ ] The project uses `/work-items`, not `/tasks`.
- [ ] The project uses `PATCH /work-items/{id}`, not `PUT`, for partial updates.
- [ ] The classifier endpoint is `POST /work-items/classify`, not `auto_prioritize=true`.
- [ ] The classifier is side-effect free and does not persist data.
- [ ] Runtime external LLM providers are out of scope.
- [ ] `.env.example` does not include `OPENAI_API_KEY`, `OPENAI_MODEL`, or LLM timeout variables.
- [ ] The project does not use `python-dotenv`.

## Documentation

- [ ] README explains the academic context.
- [ ] README maps the course task API idea to this project's work item API.
- [ ] README includes setup, run, test, API examples, troubleshooting, and limitations.
- [ ] `docs/architecture.md` includes Mermaid diagrams.
- [ ] `docs/decisions.md` explains core technical decisions.
- [ ] `docs/prompts.md` documents sanitized prompt traceability.
- [ ] `docs/backlog.md` describes releases and acceptance criteria.

## Verification

- [ ] `python -m pytest -q` passes.
- [ ] `git status --short` is clean.
- [ ] No `.db`, `.sqlite`, `.sqlite3`, `.env`, `__pycache__`, `.pytest_cache`, or local artifact is tracked by Git.
- [ ] No private working folders such as `.private/`, `private/`, or `docs/priv/` are tracked by Git.
- [ ] No private strategy files, local notes, credentials, customer data, or sensitive personal data are tracked by Git.
- [ ] No ignored private files were force-added with `git add -f`.
- [ ] `git grep` was run for sensitive path and name patterns before publication.
- [ ] Conventional Commit history is present.
- [ ] MIT License is present.

## Out Of Scope Confirmation

- [ ] No authentication.
- [ ] No frontend.
- [ ] No Docker.
- [ ] No CI/CD.
- [ ] No RAG.
- [ ] No agents.
- [ ] No queues.
- [ ] No streaming.
- [ ] No external integrations.
- [ ] No external AI provider at runtime.
