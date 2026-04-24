# micro-api-work-items

micro-api-work-items is a small academic REST API for managing work items with FastAPI, SQLite, automated tests, and local deterministic classification rules.

A work item is a generic task-like record that can represent a task, bug, improvement, research item, operation item, or incident.

## Objective

The objective is to demonstrate a simple backend MVP with clear scope, local persistence, validation, tests, documentation, and a Conventional Commit history.

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

### Standard Python/venv

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell with `python` available on `PATH`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Linux/WSL

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Anaconda Prompt

```bash
conda create -n micro-api-work-items python=3.11
conda activate micro-api-work-items
python -m pip install -r requirements.txt
```

### Windows PowerShell With Full Anaconda Path

If Python is not available directly as `python`, use the full Anaconda Python executable path:

```powershell
& 'C:\Users\<your-user>\anaconda3\python.exe' -m pip install -r requirements.txt
```

The app reads `DATABASE_URL` from the operating system environment. If it is not set, it defaults to `sqlite:///./work_items.db`.

`.env.example` is a reference file only. It is not loaded automatically, and the project does not use `python-dotenv`.

## Run

```bash
python -m uvicorn app.main:app --reload
```

With a full Anaconda Python path in Windows PowerShell:

```powershell
& 'C:\Users\<your-user>\anaconda3\python.exe' -m uvicorn app.main:app --reload
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

## Tests

```bash
python -m pytest -q
```

With a full Anaconda Python path in Windows PowerShell:

```powershell
& 'C:\Users\<your-user>\anaconda3\python.exe' -m pytest -q
```

The test suite covers health, CRUD behavior, validation errors, missing item `404` responses, tags and metadata persistence, `updated_at` behavior, and deterministic classification.

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

## Generative AI Support

Generative AI supported planning, implementation structure, test coverage design, documentation drafting, and review against the acceptance checklist. The project intentionally uses only local deterministic rules at runtime and does not depend on any external AI provider.

See `docs/prompts.md` for generic CO-STAR prompt examples used for academic reproducibility.
