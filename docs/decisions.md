# Decisions

## SQLite For Local Persistence

SQLite keeps the MVP simple to run locally while still demonstrating relational persistence through SQLAlchemy.

## FastAPI And Pydantic v2

FastAPI provides concise routing and OpenAPI generation. Pydantic v2 provides request and response validation with enum-backed fields.

## SQLAlchemy Model Metadata Field

SQLAlchemy reserves the `metadata` attribute on declarative models. The database column is still named `metadata`, but the Python model uses `metadata_json` internally and the API exposes `metadata`.

## PATCH Only For Updates

The MVP uses `PATCH /work-items/{id}` for partial updates. `PUT` is intentionally not included.

## Separate Classifier Flow

`POST /work-items/classify` is side-effect free. It receives input data, applies local rules, and returns suggestions without reading or writing persisted work items.

## Local Deterministic Classification

Classification uses keyword rules only. The MVP does not include external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, frontend, authentication, or external integrations.

## Environment Variables

The application reads environment variables from the operating system. `.env.example` is reference documentation only, and the project does not use `python-dotenv`.
