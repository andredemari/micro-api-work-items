# micro-api-work-items

micro-api-work-items is a small academic REST API for managing work items with FastAPI, SQLite, automated tests, and local deterministic classification rules.

A work item is a generic task-like record that can represent a task, bug, improvement, research item, operation item, or incident.

## Objective

The objective is to demonstrate a simple backend MVP with clear scope, local persistence, validation, tests, documentation, and a Conventional Commit history.

## Academic Context

This repository was created as an AI-assisted mini-project for the first practical activity of the postgraduate course "Software Engineering with Generative AI" at UFG/AKCIT.

The course reference problem is a "Micro-API de Tarefas". This repository implements the same small API idea using the more generic term "work item", so the API can represent tasks, bugs, improvements, research items, operation items, and incidents without becoming domain-specific.

| Course operation | This project |
| --- | --- |
| Criar tarefa | `POST /work-items` |
| Listar tarefas | `GET /work-items` |
| Atualizar status/prioridade | `PATCH /work-items/{id}` |
| Excluir tarefa | `DELETE /work-items/{id}` |
| Sugerir prioridade/classificação | `POST /work-items/classify` |

The course PriorityAdvisor concept is represented by the local deterministic classifier. Runtime integration with external AI providers is intentionally out of scope for this MVP.

## Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- SQLAlchemy
- SQLite
- Uvicorn
- Pytest
- HTTPX through FastAPI testing utilities

## Setup

Choose one setup path. Windows users with Anaconda should usually start with Anaconda Prompt.

Python available on PATH means the terminal can run Python by typing python. If that does not work, use Anaconda Prompt or the full Python executable path.

### Recommended For Windows Users With Anaconda: Anaconda Prompt

```bash
conda create -n micro-api-work-items python=3.11
conda activate micro-api-work-items
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --reload
```

### Alternative: Windows PowerShell With Full Anaconda Python Path

If `python` is not available directly in PowerShell, use the full Anaconda Python executable path:

```powershell
$PY="C:\Users\<your-user>\anaconda3\python.exe"
& $PY -m pip install -r requirements.txt
& $PY -m pytest -q
& $PY -m uvicorn app.main:app --reload
```

If you use a dedicated Conda environment, the full path may be:

```powershell
$PY="C:\Users\<your-user>\anaconda3\envs\micro-api-work-items\python.exe"
```

### Alternative: Standard Python Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell with `python` available:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Alternative: Linux/WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

The app reads `DATABASE_URL` from the operating system environment. If it is not set, it defaults to `sqlite:///./data/work_items.db`.

`.env.example` is a reference file only. It is not loaded automatically, and the project does not use `python-dotenv`.

The application does not use a runtime external LLM provider. No `OPENAI_API_KEY`, model name, or LLM timeout configuration is required.

## Run

```bash
python -m uvicorn app.main:app --reload
```

With a full Anaconda Python path in Windows PowerShell:

```powershell
$PY="C:\Users\<your-user>\anaconda3\python.exe"
& $PY -m uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Examples

The `curl` examples below are intended for Bash, Git Bash, macOS/Linux terminals, WSL, or real `curl.exe`. In Windows PowerShell, `curl` may resolve to `Invoke-WebRequest`; use the PowerShell examples in the next section if needed.

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Create a work item:

```bash
curl -X POST http://127.0.0.1:8000/work-items \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix validation error",
    "description": "Review the validation response for a small API issue.",
    "priority": "high",
    "type": "bug",
    "tags": ["api", "validation"],
    "metadata": {"estimate": 2}
  }'
```

List work items:

```bash
curl http://127.0.0.1:8000/work-items
```

Get one work item:

```bash
curl http://127.0.0.1:8000/work-items/1
```

Partially update a work item:

```bash
curl -X PATCH http://127.0.0.1:8000/work-items/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress", "priority": "critical"}'
```

Delete a work item:

```bash
curl -X DELETE http://127.0.0.1:8000/work-items/1
```

Classify a work item without persisting it:

```bash
curl -X POST http://127.0.0.1:8000/work-items/classify \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Critical incident with service outage",
    "description": "The service is unavailable for users.",
    "tags": ["support"]
  }'
```

## Windows PowerShell API Examples

Health check:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health'
```

Create a work item:

```powershell
$body = @{
  title = 'Fix validation error'
  description = 'Review the validation response for a small API issue.'
  priority = 'high'
  type = 'bug'
  tags = @('api', 'validation')
  metadata = @{ estimate = 2 }
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri 'http://127.0.0.1:8000/work-items' `
  -Method Post `
  -ContentType 'application/json' `
  -Body $body
```

List work items:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items'
```

Partially update a work item:

```powershell
$body = @{
  status = 'in_progress'
  priority = 'critical'
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri 'http://127.0.0.1:8000/work-items/1' `
  -Method Patch `
  -ContentType 'application/json' `
  -Body $body
```

Classify a work item without persisting it:

```powershell
$body = @{
  title = 'Critical incident with service outage'
  description = 'The service is unavailable for users.'
  tags = @('support')
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri 'http://127.0.0.1:8000/work-items/classify' `
  -Method Post `
  -ContentType 'application/json' `
  -Body $body
```

## Response Examples

Successful work item creation returns `201 Created`. The `id`, `created_at`, and `updated_at` values are generated by the API.

```json
{
  "title": "Fix validation error",
  "description": "Review the validation response for a small API issue.",
  "status": "open",
  "priority": "high",
  "type": "bug",
  "source": "manual",
  "tags": ["api", "validation"],
  "metadata": {"estimate": 2},
  "id": 1,
  "created_at": "2026-04-24T12:00:00",
  "updated_at": "2026-04-24T12:00:00"
}
```

Missing work items return `404 Not Found`:

```json
{
  "detail": "Work item not found."
}
```

Invalid enum values return FastAPI's standard `422 Unprocessable Entity` validation response. For example, sending `"status": "waiting"` returns:

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "status"],
      "msg": "Input should be 'open', 'in_progress', 'done' or 'archived'",
      "input": "waiting",
      "ctx": {
        "expected": "'open', 'in_progress', 'done' or 'archived'"
      }
    }
  ]
}
```

## Tests

```bash
python -m pytest -q
```

With a full Anaconda Python path in Windows PowerShell:

```powershell
$PY="C:\Users\<your-user>\anaconda3\python.exe"
& $PY -m pytest -q
```

The test suite covers health, CRUD behavior, validation errors, missing item `404` responses, tags and metadata persistence, `updated_at` behavior, and deterministic classification.

## Reset Local SQLite State

The default local database file is `data/work_items.db`. Stop the API server before deleting it.

In Bash, Git Bash, macOS/Linux terminals, or WSL:

```bash
rm -f data/work_items.db
```

In Windows PowerShell:

```powershell
Remove-Item -LiteralPath .\data\work_items.db -ErrorAction SilentlyContinue
```

The next application startup recreates the SQLite schema automatically.

## Troubleshooting

- If `python` is not recognized in PowerShell, use Anaconda Prompt or the full Anaconda Python executable path shown in the setup section.
- If `uvicorn` is not recognized, run it as a module with `python -m uvicorn app.main:app --reload`.
- If `curl` behaves differently in PowerShell, use the `Invoke-RestMethod` examples instead.
- If the API returns database-related errors after manual file changes, stop the server, remove `data/work_items.db`, and start the server again.
- `.env.example` is documentation only; environment variables must be set in the operating system if you want to override defaults.
- No runtime external LLM provider is used, so no AI provider credentials are needed.

## Limitations

- Local SQLite persistence only.
- Hard delete only.
- No authentication or authorization.
- No pagination or advanced filtering.
- Local keyword-based classification only.
- No external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, frontend, or external integrations.

## Next Steps

- Add pagination and simple filters for list endpoints.
- Add Alembic migrations if schema evolution becomes necessary.
- Add richer validation rules for tags and metadata.
- Add deployment documentation for a non-local environment.

Future versions may expose the API as a reusable backend service for external clients, automation scripts, or agent-based tools through its HTTP/OpenAPI interface.

## How Generative AI Was Used

Generative AI supported planning, scope definition, architecture discussion, implementation structure, test design, documentation drafting, review, and refinement. The project intentionally uses only local deterministic rules at runtime and does not depend on any external AI provider.

Final decisions, validation, testing, and acceptance were human-reviewed before inclusion in the repository.

See `docs/prompts.md` for generic CO-STAR prompt examples used for academic reproducibility.

## License

This project is licensed under the [MIT License](LICENSE).
