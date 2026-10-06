# API Examples

This document keeps detailed request and response examples outside the main README so the project overview stays concise.

Choose examples for your terminal: [Anaconda Prompt and Windows CMD](#anaconda-prompt-and-windows-cmd), [Bash and compatible shells](#bash-git-bash-macoslinux-or-wsl), or [Windows PowerShell](#windows-powershell). Quoting depends on the shell, even when using the real `curl.exe`. In Windows PowerShell, `curl` may resolve to `Invoke-WebRequest`; use the `Invoke-RestMethod` examples below.

`GET /work-items` accepts these optional scalar query parameters:

| Parameter | Allowed values |
| --- | --- |
| `status` | `open`, `in_progress`, `done`, `archived` |
| `priority` | `low`, `medium`, `high`, `critical` |

Both filters combine with AND. Omitting a parameter leaves that attribute unrestricted; omitting both returns the same list of complete objects as before, ordered by ascending ID. All successful list requests return `200`, including `[]` for no matches or an empty database. Queries do not modify stored records or timestamps.

Compatibility change: `status` and `priority` were previously ignored on this endpoint. They now restrict results or produce FastAPI's standard `422` query validation error. Omission is different from an empty value (`status=`) or the literal text `null` (`status=null`); neither is an allowed enum value. The same rule applies to `priority`. Repeated parameters remain scalar: FastAPI uses and validates the last occurrence, rather than creating a list or combining values with OR.

## Anaconda Prompt And Windows CMD

Use this section in the standard Anaconda Prompt, which uses Windows CMD. Execute each command on one line. CMD does not use single quotes to group arguments: use double quotes for the header and URL, and escape the double quotes inside JSON with `\"`. Bash commands copied into CMD can produce an invalid request body and `Could not resolve host: application`.

### Start With A Separate Test Database

Open a new Anaconda Prompt, activate your existing project environment, and enter the checkout. Replace the environment and folder below with your existing values; do not reinstall dependencies just to run these examples.

```bat
conda activate micro-api-work-items
cd /d "D:\path\to\micro-api-work-items"
for /f %I in ('python -c "import uuid; print(uuid.uuid4().hex)"') do set "WORKITEMS_MANUAL_DIR=%TEMP%\work-items-manual-%I"
set "DATABASE_URL=sqlite:///%WORKITEMS_MANUAL_DIR:\=/%/manual.sqlite3"
python -m uvicorn app.main:app --host 127.0.0.1 --port 0 --workers 1
```

This creates a new temporary SQLite database and lets the operating system choose a free port. Wait for `Application startup complete`. Keep this terminal open. In a second Anaconda Prompt, set the URL to the actual address printed by Uvicorn. For example, use the following only if its log shows port `54321`:

```bat
set "WORKITEMS_URL=http://127.0.0.1:54321"
```

If you already have a server using a separate test database at port `8000`, set its URL directly:

```bat
set "WORKITEMS_URL=http://127.0.0.1:8000"
```

Before creating items, run the unfiltered query first. In the new database, both commands should return `HTTP 200` and `[]`:

```bat
curl.exe -i "%WORKITEMS_URL%/work-items"
curl.exe -i "%WORKITEMS_URL%/work-items?status=open&priority=high"
```

An empty unfiltered response only confirms the absence of work items at that moment; it does not prove that this server uses an isolated database. Confirm that the server was started with the separate database configuration above. If the unfiltered response contains items, do not run the POSTs: repeat the setup with a new UUID and use that new server's actual URL. Do not delete existing data to make the examples pass.

### Create A, B, C, And D Individually

Run each POST once. Each returns `HTTP 201` and the complete created object, including its ID and timestamps. The following commands are for CMD, including Anaconda Prompt:

```bat
curl.exe -i -X POST "%WORKITEMS_URL%/work-items" -H "Content-Type: application/json" -d "{\"title\":\"A\",\"status\":\"open\",\"priority\":\"high\"}"
curl.exe -i -X POST "%WORKITEMS_URL%/work-items" -H "Content-Type: application/json" -d "{\"title\":\"B\",\"status\":\"open\",\"priority\":\"low\"}"
curl.exe -i -X POST "%WORKITEMS_URL%/work-items" -H "Content-Type: application/json" -d "{\"title\":\"C\",\"status\":\"done\",\"priority\":\"high\"}"
curl.exe -i -X POST "%WORKITEMS_URL%/work-items" -H "Content-Type: application/json" -d "{\"title\":\"D\",\"status\":\"in_progress\",\"priority\":\"critical\"}"
```

### Try Each Filter

```bat
curl.exe -i "%WORKITEMS_URL%/work-items"
curl.exe -i "%WORKITEMS_URL%/work-items?status=open"
curl.exe -i "%WORKITEMS_URL%/work-items?priority=high"
curl.exe -i "%WORKITEMS_URL%/work-items?status=open&priority=high"
curl.exe -i "%WORKITEMS_URL%/work-items?status=archived&priority=critical"
curl.exe -i "%WORKITEMS_URL%/work-items?status=done&status=open"
curl.exe -i "%WORKITEMS_URL%/work-items?priority=low&priority=high"
```

Assuming this database contains only A–D, each query returns `HTTP 200` with these complete objects in ascending ID order. The letters below are shorthand for objects, not a changed response format; see [List Filter Examples](#list-filter-examples) for full JSON responses.

| Query | Expected objects |
| --- | --- |
| No filters | A, B, C, D |
| `status=open` | A, B |
| `priority=high` | A, C |
| `status=open&priority=high` | A |
| `status=archived&priority=critical` | `[]` |
| `status=done&status=open` | A, B |
| `priority=low&priority=high` | A, C |

### Try Validation Errors

Each command below should return `HTTP 422`. Its `detail` identifies `["query", "status"]` or `["query", "priority"]`, including the invalid last value for a repeated parameter.

```bat
curl.exe -i "%WORKITEMS_URL%/work-items?status=testing"
curl.exe -i "%WORKITEMS_URL%/work-items?priority=urgent"
curl.exe -i "%WORKITEMS_URL%/work-items?status="
curl.exe -i "%WORKITEMS_URL%/work-items?priority="
curl.exe -i "%WORKITEMS_URL%/work-items?status=null"
curl.exe -i "%WORKITEMS_URL%/work-items?priority=null"
curl.exe -i "%WORKITEMS_URL%/work-items?status=open&status=testing"
curl.exe -i "%WORKITEMS_URL%/work-items?priority=high&priority=urgent"
```

Repeat `GET /work-items` to check that the same four objects and timestamps remain. To end this test server, press `Ctrl+C` in the first terminal, then close the new prompts to discard their local environment variables. The temporary database is preserved. Starting the setup again creates another new database; do not delete an existing database to repeat these examples. `%I` above is for the interactive prompt; batch files use `%%I`.

### Pytest Temporary Directory Permission Error In CMD

If `python -m pytest -q` fails with `PermissionError` or `WinError 5` mentioning `pytest-current`, run the suite with a new temporary directory. Use an Anaconda Prompt already in the project checkout with your existing environment activated. These automated tests do not require a running server.

```bat
for /f %I in ('python -c "import uuid; print(uuid.uuid4().hex)"') do set "WORKITEMS_TEST_TMP=%TEMP%\work-items-pytest-%I"
python -m pytest -q --basetemp "%WORKITEMS_TEST_TMP%" -p no:cacheprovider
echo Exit code: %ERRORLEVEL%
```

Generate a new UUID before every run. pytest removes an existing `--basetemp` directory before using it, so use the existing `%TEMP%` parent and a new GUID-named child as shown; never point it at a database, checkout, or another directory containing data. These pytest options apply only to this command. `%I` is for an interactive prompt; batch files use `%%I`.

## Bash, Git Bash, macOS/Linux, Or WSL

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

### Create A Work Item

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

### List Work Items

```bash
curl http://127.0.0.1:8000/work-items
```

Individual filters, an AND combination, and a valid query with no matches:

```bash
curl 'http://127.0.0.1:8000/work-items?status=open'
curl 'http://127.0.0.1:8000/work-items?priority=high'
curl 'http://127.0.0.1:8000/work-items?status=open&priority=high'
curl 'http://127.0.0.1:8000/work-items?status=archived&priority=critical'
```

Repeated parameters use the last value. With the synthetic items below, these return A/B and A/C respectively:

```bash
curl 'http://127.0.0.1:8000/work-items?status=done&status=open'
curl 'http://127.0.0.1:8000/work-items?priority=low&priority=high'
```

### Get One Work Item

```bash
curl http://127.0.0.1:8000/work-items/1
```

### Partially Update A Work Item

```bash
curl -X PATCH http://127.0.0.1:8000/work-items/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress", "priority": "critical"}'
```

### Delete A Work Item

```bash
curl -X DELETE http://127.0.0.1:8000/work-items/1
```

### Classify Without Persisting

```bash
curl -X POST http://127.0.0.1:8000/work-items/classify \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Critical incident with service outage",
    "description": "The service is unavailable for users.",
    "tags": ["support"]
  }'
```

## Windows PowerShell

### Health Check

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health'
```

### Create A Work Item

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

### List Work Items

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items'
```

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items?status=open'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items?priority=high'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items?status=open&priority=high'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items?status=archived&priority=critical'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items?status=done&status=open'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items?priority=low&priority=high'
```

### Get One Work Item

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items/1'
```

### Partially Update A Work Item

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

### Delete A Work Item

```powershell
Invoke-RestMethod `
  -Uri 'http://127.0.0.1:8000/work-items/1' `
  -Method Delete
```

### Classify Without Persisting

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

### Successful Creation

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

### List Filter Examples

This independent example set uses an empty disposable database and four synthetic items created in order. It does not reuse the earlier creation example. For complete Anaconda Prompt/Windows CMD commands that set `DATABASE_URL` to a new temporary database and start a server on a free port, follow [Start With A Separate Test Database](#start-with-a-separate-test-database). Use a separate test database for these examples.

The Bash and PowerShell requests in this section use `http://127.0.0.1:8000`. Replace that base URL with the actual address printed by your separate test server; the setup above uses `--port 0` and does not guarantee port `8000`. Confirm the server's explicit database configuration before sending requests; a server started without a `DATABASE_URL` override may use the default `data/work_items.db`.

The creation commands immediately below use Bash quoting. For Anaconda Prompt, use [Create A, B, C, And D Individually](#create-a-b-c-and-d-individually) in the CMD section instead.

```bash
curl -X POST http://127.0.0.1:8000/work-items -H 'Content-Type: application/json' -d '{"title":"A","status":"open","priority":"high"}'
curl -X POST http://127.0.0.1:8000/work-items -H 'Content-Type: application/json' -d '{"title":"B","status":"open","priority":"low"}'
curl -X POST http://127.0.0.1:8000/work-items -H 'Content-Type: application/json' -d '{"title":"C","status":"done","priority":"high"}'
curl -X POST http://127.0.0.1:8000/work-items -H 'Content-Type: application/json' -d '{"title":"D","status":"in_progress","priority":"critical"}'
```

Equivalent creation requests in PowerShell:

```powershell
$items = @(
  @{ title = 'A'; status = 'open'; priority = 'high' }
  @{ title = 'B'; status = 'open'; priority = 'low' }
  @{ title = 'C'; status = 'done'; priority = 'high' }
  @{ title = 'D'; status = 'in_progress'; priority = 'critical' }
)
foreach ($item in $items) {
  Invoke-RestMethod -Uri 'http://127.0.0.1:8000/work-items' -Method Post `
    -ContentType 'application/json' -Body ($item | ConvertTo-Json)
}
```

Each creation returns `201`. IDs below assume this empty database. Timestamps are illustrative; use each actual creation response when comparing objects. Omitted creation fields use the existing defaults shown below.

`GET /work-items` returns `200` with A, B, C, and D:

```json
[
  {"title":"A","description":"","status":"open","priority":"high","type":"task","source":"manual","tags":[],"metadata":null,"id":1,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"},
  {"title":"B","description":"","status":"open","priority":"low","type":"task","source":"manual","tags":[],"metadata":null,"id":2,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"},
  {"title":"C","description":"","status":"done","priority":"high","type":"task","source":"manual","tags":[],"metadata":null,"id":3,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"},
  {"title":"D","description":"","status":"in_progress","priority":"critical","type":"task","source":"manual","tags":[],"metadata":null,"id":4,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"}
]
```

`GET /work-items?status=open` returns `200` with the complete A and B objects:

```json
[
  {"title":"A","description":"","status":"open","priority":"high","type":"task","source":"manual","tags":[],"metadata":null,"id":1,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"},
  {"title":"B","description":"","status":"open","priority":"low","type":"task","source":"manual","tags":[],"metadata":null,"id":2,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"}
]
```

`GET /work-items?priority=high` returns `200` with the complete A and C objects:

```json
[
  {"title":"A","description":"","status":"open","priority":"high","type":"task","source":"manual","tags":[],"metadata":null,"id":1,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"},
  {"title":"C","description":"","status":"done","priority":"high","type":"task","source":"manual","tags":[],"metadata":null,"id":3,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"}
]
```

`GET /work-items?status=open&priority=high` returns `200` with only the complete A object:

```json
[
  {"title":"A","description":"","status":"open","priority":"high","type":"task","source":"manual","tags":[],"metadata":null,"id":1,"created_at":"2026-04-24T12:00:00","updated_at":"2026-04-24T12:00:00"}
]
```

`GET /work-items?status=archived&priority=critical` returns `200` with:

```json
[]
```

An empty database also returns `200` with `[]` for any valid combination, for example `GET /work-items?status=open&priority=high`.

The repeated queries `status=done&status=open` and `priority=low&priority=high` return the same complete objects as their single-filter examples above. `status=done&status=open&priority=low&priority=high` returns only A: the last value of each parameter is applied with AND.

### List Query Validation Errors

For example, run these requests with `curl -i` to see the status and JSON response:

```bash
curl -i 'http://127.0.0.1:8000/work-items?status=testing'
curl -i 'http://127.0.0.1:8000/work-items?priority=urgent'
```

Both return `422`. Their standard FastAPI response shapes are shown below; exact message wording can vary by FastAPI/Pydantic version.

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["query", "status"],
      "msg": "Input should be 'open', 'in_progress', 'done' or 'archived'",
      "input": "testing",
      "ctx": {"expected": "'open', 'in_progress', 'done' or 'archived'"}
    }
  ]
}
```

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["query", "priority"],
      "msg": "Input should be 'low', 'medium', 'high' or 'critical'",
      "input": "urgent",
      "ctx": {"expected": "'low', 'medium', 'high' or 'critical'"}
    }
  ]
}
```

These additional request suffixes have the same `422` enum error shape with the indicated `loc` and `input`. Append them to `http://127.0.0.1:8000/work-items` in `curl -i` or `Invoke-RestMethod` (PowerShell reports non-success HTTP responses as errors).

| Query suffix | Expected `loc` | Expected `input` |
| --- | --- | --- |
| `?status=` | `["query", "status"]` | `""` |
| `?priority=` | `["query", "priority"]` | `""` |
| `?status=null` | `["query", "status"]` | `"null"` |
| `?priority=null` | `["query", "priority"]` | `"null"` |
| `?status=open&status=testing` | `["query", "status"]` | `"testing"` |
| `?priority=high&priority=urgent` | `["query", "priority"]` | `"urgent"` |
| `?status=open&status=` | `["query", "status"]` | `""` |
| `?priority=high&priority=` | `["query", "priority"]` | `""` |
| `?status=open&status=null` | `["query", "status"]` | `"null"` |
| `?priority=high&priority=null` | `["query", "priority"]` | `"null"` |

If an earlier occurrence is invalid but the last one is valid, only the last one is validated: `status=testing&status=open` returns A/B and `priority=urgent&priority=high` returns A/C. Sending an invalid filter to an empty database still returns `422`.

### Missing Work Item

Missing work items return `404 Not Found`:

```json
{
  "detail": "Work item not found."
}
```

### Validation Error

Invalid enum values return FastAPI's standard `422 Unprocessable Entity` validation response. Exact wording may vary slightly by FastAPI or Pydantic version, but the response includes a `detail` list describing the invalid field.

Example request:

```bash
curl -X POST http://127.0.0.1:8000/work-items \
  -H "Content-Type: application/json" \
  -d '{"title": "Invalid work item", "status": "waiting"}'
```

Example response shape:

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "status"],
      "msg": "Input should be one of the allowed status values",
      "input": "waiting"
    }
  ]
}
```
