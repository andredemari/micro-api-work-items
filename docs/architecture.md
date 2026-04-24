# Architecture

micro-api-work-items is a small FastAPI backend organized around a simple layered architecture.

## Layers

- API routes receive HTTP requests and return response schemas.
- Pydantic schemas validate request and response data.
- Services hold application logic for persisted work items and local classification.
- SQLAlchemy models define local SQLite persistence.
- Tests validate API behavior and deterministic rules.

```mermaid
flowchart TD
    Client["HTTP client"] --> Routes["FastAPI routes"]
    Routes --> Schemas["Pydantic schemas"]
    Routes --> Services["Application services"]
    Services --> Models["SQLAlchemy models"]
    Models --> SQLite["SQLite database"]
    Tests["Pytest suite"] --> Routes
    Tests --> Services
```

## Request Flow

1. A client calls a FastAPI endpoint.
2. The route validates input using Pydantic schemas.
3. CRUD routes use the work item service and a SQLAlchemy session.
4. The service reads or writes SQLite data through SQLAlchemy models.
5. The route returns a Pydantic response model.

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI CRUD route
    participant Schema as Pydantic schema
    participant Service as Work item service
    participant DB as SQLite via SQLAlchemy

    Client->>API: POST/GET/PATCH/DELETE /work-items
    API->>Schema: Validate request or response
    API->>Service: Call CRUD operation
    Service->>DB: Read or write work item
    DB-->>Service: Return model data
    Service-->>API: Return result
    API-->>Client: JSON response or status code
```

The classifier endpoint follows a separate flow: it validates input, applies local deterministic rules, and returns suggestions without writing to the database.

```mermaid
sequenceDiagram
    participant Client
    participant API as Classifier route
    participant Schema as Pydantic schema
    participant Rules as Local rule engine

    Client->>API: POST /work-items/classify
    API->>Schema: Validate input
    API->>Rules: Apply deterministic keyword rules
    Rules-->>API: Return suggestions and reasons
    API-->>Client: JSON classification response
```

## Persistence

The MVP uses SQLite through SQLAlchemy. The application reads `DATABASE_URL` from the operating system environment and defaults to `sqlite:///./work_items.db`.

The project does not use `python-dotenv`; `.env.example` is only a reference file.

## API Routes

- `GET /health`
- `POST /work-items`
- `GET /work-items`
- `GET /work-items/{id}`
- `PATCH /work-items/{id}`
- `DELETE /work-items/{id}`
- `POST /work-items/classify`
