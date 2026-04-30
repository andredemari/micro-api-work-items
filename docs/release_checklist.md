# Release Checklist

Use this checklist before submitting the academic MVP. Checked items reflect
the final verification commands run before creating
`docs/final_delivery_report.md`.

## Scope

- [x] The project uses `/work-items`, not `/tasks`.
- [x] The project uses `PATCH /work-items/{id}`, not `PUT`, for partial updates.
- [x] The classifier endpoint is `POST /work-items/classify`, not `auto_prioritize=true`.
- [x] The classifier is side-effect free and does not persist data.
- [x] Runtime external LLM providers are out of scope.
- [x] `.env.example` does not include `OPENAI_API_KEY`, `OPENAI_MODEL`, or LLM timeout variables.
- [x] The project does not use `python-dotenv`.

## Documentation

- [x] README explains the academic context.
- [x] README maps the course task API idea to this project's work item API.
- [x] README includes setup, run, test, API examples, troubleshooting, and limitations.
- [x] `docs/architecture.md` includes Mermaid diagrams.
- [x] `docs/decisions.md` explains core technical decisions in lightweight ADR style.
- [x] `docs/prompts.md` documents sanitized CO-STAR-style prompt traceability.
- [x] `docs/backlog.md` describes releases and acceptance criteria.
- [x] `docs/course_submission_traceability.md` maps course expectations to repository evidence.
- [x] `docs/final_delivery_report.md` records final delivery evidence.

## Verification

- [x] `python -m pytest -q` passes with `59 passed`.
- [x] `python scripts/safety_check.py` exits successfully with only the release reminder warning.
- [x] `git status --short --branch` was clean before the final evidence patch.
- [x] `git log --oneline --max-count=15` shows recent Conventional Commit evidence.
- [x] `git ls-files` confirms the tracked source/documentation/test tree.
- [x] `git tag --list` returned no existing tags before publication/tagging.
- [x] `git remote -v` returned no configured remotes before publication.
- [x] No `.db`, `.sqlite`, `.sqlite3`, `.env`, `__pycache__`, `.pytest_cache`, or local artifact is tracked by Git.
- [x] No private working folders such as `.private/`, `private/`, or `docs/priv/` are tracked by Git.
- [x] No private strategy files, local notes, credentials, customer data, or sensitive personal data are tracked by Git.
- [x] Local presentation notes remain ignored and untracked; `docs/demo.md` is not part of the public tracked submission.
- [x] No ignored private files were force-added with `git add -f`.
- [x] The deterministic safety checker was run before publication or packaging.
- [x] Apache License 2.0 / Apache-2.0 is present.

## Out Of Scope Confirmation

- [x] No authentication.
- [x] No frontend.
- [x] No Docker.
- [x] No CI/CD.
- [x] No RAG.
- [x] No GraphRAG.
- [x] No agents.
- [x] No MCP integration.
- [x] No sandboxing or script execution services.
- [x] No queues.
- [x] No streaming.
- [x] No external integrations.
- [x] No external AI provider at runtime.
- [x] No local LLM runtime integration.
- [x] No parent-governance internals or private-memory material.

## Publication And Submission Still Pending

- [ ] Public GitHub remote created.
- [ ] Repository pushed or synced to GitHub.
- [ ] Final release tag created.
- [ ] Course submission completed.

## Packaging

- [x] Recommended packaging method is tracked-file archive:

```bash
git archive --format=zip --output micro-api-work-items.zip HEAD
```

- [x] Manual ZIP of the whole working directory is not recommended because it
  can include ignored local files.
