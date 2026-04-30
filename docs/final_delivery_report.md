# Final Course Delivery Report

Prepared for the final course submission evidence package.

## 1. Project Objective

`micro-api-work-items` is a small academic REST API for managing generic work
items. It demonstrates a local FastAPI backend with validation, SQLite
persistence, automated tests, deterministic priority/classification
suggestions, public documentation, and release-safety checks.

The course reference problem is a "Micro-API de Tarefas". This implementation
uses the broader term "work item" so the same API can represent tasks, bugs,
improvements, research items, operation items, and incidents.

## 2. Final MVP Scope Delivered

Delivered scope:

- `GET /health` health check.
- CRUD operations under `/work-items`.
- Partial update with `PATCH /work-items/{id}`.
- Side-effect-free `POST /work-items/classify` suggestion endpoint.
- Local SQLite persistence through SQLAlchemy.
- Pydantic v2 request and response schemas.
- Layered organization with controllers, schemas, services, repositories,
  models, database setup, and a local deterministic provider boundary.
- Automated API, service, repository, provider, PriorityAdvisor, and
  safety-check tests.
- Public-safe documentation and deterministic pre-publication safety check.

## 3. Tracked File Tree Summary

The tracked repository tree is intentionally small and source-focused. Based on
`git ls-files`, the submission contains the following groups:

```text
root/
  .env.example
  .gitignore
  LICENSE
  Makefile
  README.md
  requirements.txt

app/
  controllers/
  db/
  models/
  providers/
  repositories/
  schemas/
  services/
  main.py

data/
  .gitkeep

docs/
  api_examples.md
  architecture.md
  backlog.md
  course_submission_traceability.md
  decisions.md
  external_provider_plan.md
  final_delivery_report.md
  information_governance.md
  local_llm_setup.md
  mvp_scope.md
  prompts.md
  refactor_backlog.md
  release_checklist.md
  security_checks.md
  security_cleanup_runbook.md

scripts/
  install_git_hooks.py
  safety_check.py
  safety_policy.json

tests/
  conftest.py
  test_classifier.py
  test_health.py
  test_local_priority_provider.py
  test_priority_advisor_service.py
  test_safety_check.py
  test_work_item_repository.py
  test_work_items_api.py
  test_work_items_service.py
```

Runtime databases, virtual environments, Python caches, pytest caches,
generated archives, local environment files, and local presentation notes are
not part of the tracked submission.

## 4. Git Status Result

Final verification before writing this report:

```text
git status --short --branch
## master
```

The working tree was clean before creating this final evidence patch.

## 5. Recent Git Log Evidence

Recent Conventional Commit history from `git log --oneline --max-count=15`:

```text
b48308d docs: improve pre-tag documentation clarity
6dcf08f docs: switch project license to Apache 2.0
813ea46 docs: refine course submission traceability
05123fd docs: add course submission traceability
a5e0ede chore: improve safety gate portability
60fcf77 docs: clarify safety check portability
d24ca6c test: cover safety check hardening
428bf3a chore: harden deterministic safety check
39dee15 docs: document safety check workflow
37df73c test: add safety check coverage
948644e chore: add deterministic safety check
bda5d1c docs: add security governance and cleanup runbook
6e582ad docs: remove private demo references
6044671 merge: integrate external provider planning
2322d3e docs: add external provider planning guidance
```

## 6. Pytest Command And Result

Command:

```bash
python -m pytest -q
```

Result:

```text
59 passed
```

## 7. Safety-Check Command And Result

Command:

```bash
python scripts/safety_check.py
```

Result:

```text
Passed with release reminder warning only.
```

The warning reminds the maintainer to confirm remote visibility, old commits,
and `git archive` packaging before publication. It is not a failure.

## 8. Run Command

Install dependencies and start the API locally:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

## 9. API Example References

Detailed Bash, curl, and Windows PowerShell API examples are documented in:

- `docs/api_examples.md`

The README also includes a compact example flow for:

- `GET /health`;
- `POST /work-items`;
- `GET /work-items`;
- `POST /work-items/classify`.

## 10. Course Traceability Reference

Course expectations are mapped to repository artifacts in:

- `docs/course_submission_traceability.md`

That document links the course task idea to the delivered FastAPI routes,
layered architecture, SQLite persistence, tests, documentation, AI-use
statement, release checks, and explicit out-of-scope boundaries.

## 11. License Statement

The project is licensed under Apache License 2.0 / Apache-2.0.

The full license text is tracked in:

- `LICENSE`

## 12. Limitations

- Local SQLite persistence only.
- Integer IDs are used for the local course MVP.
- Hard delete only.
- No pagination or advanced filtering.
- Local keyword-based PriorityAdvisor suggestions only.
- No production deployment configuration.
- No authentication or authorization.
- No frontend.
- No Docker.
- No CI/CD.

## 13. Explicit Out Of Scope

The following are intentionally out of scope for this course MVP:

- external AI providers at runtime;
- local LLM runtime integration;
- embeddings;
- RAG or GraphRAG;
- autonomous agents;
- MCP integration;
- sandboxing or script execution services;
- queues;
- streaming;
- external integrations;
- enterprise modules;
- additional databases;
- parent-governance internals;
- private-memory material.

## 14. Packaging Recommendation

Prefer publishing the GitHub repository or creating a ZIP from tracked files:

```bash
git archive --format=zip --output micro-api-work-items.zip HEAD
```

Do not manually ZIP the whole working directory. A manual ZIP may include
ignored local files such as `.venv/`, `__pycache__/`, `.pytest_cache/`, local
SQLite databases, local environment files, or generated archives.

## 15. Local Demo Note

`docs/demo.md` is intentionally ignored and local-only. It may exist on the
maintainer's machine as presentation material for a short demo, but it is not
tracked, staged, committed, or part of the public GitHub/course submission.
