# Decisions

## SQLite For Local Persistence

SQLite keeps the MVP simple to run locally while still demonstrating relational persistence through SQLAlchemy.

## FastAPI And Pydantic v2

FastAPI provides concise routing and OpenAPI generation. Pydantic v2 provides request and response validation with enum-backed fields.

## Why FastAPI, Pydantic and SQLAlchemy

FastAPI was chosen because the MVP is an API-first backend and FastAPI provides concise route declaration and automatic OpenAPI documentation.

Pydantic v2 is used for request and response validation, making the API contract explicit and easier to test.

SQLAlchemy is used for persistence with SQLite, keeping the project local and simple while demonstrating a relational data model.

Flask would also be a valid option for a small API, but FastAPI was chosen because it reduces boilerplate for validation and documentation, which is useful for an academic micro-API MVP.

## SQLAlchemy Model Metadata Field

SQLAlchemy reserves the `metadata` attribute on declarative models. The database column is still named `metadata`, but the Python model uses `metadata_json` internally and the API exposes `metadata`.

## Repository Layer Deferred For MVP

An explicit `app/repositories/work_items.py` layer was considered, but it would mostly add indirection for the current MVP. The service layer currently performs a small set of simple SQLAlchemy operations, so keeping that access local is easier to read for an introductory academic project.

This decision can be revisited if persistence logic grows, if multiple storage backends are introduced, or if repository-level tests become more useful than the current service/API test boundary.

## PATCH Only For Updates

The MVP uses `PATCH /work-items/{id}` for partial updates. `PUT` is intentionally not included.

## Separate PriorityAdvisor Flow

`POST /work-items/classify` is side-effect free. It receives input data, delegates to the local PriorityAdvisor, applies deterministic rules, and returns suggestions without reading or writing persisted work items.

## Local Deterministic PriorityAdvisor

Classification uses keyword rules only. The MVP does not include external AI providers, LLM APIs, embeddings, RAG, agents, queues, streaming, frontend, authentication, or external integrations.

## External AI Runtime Integration Deferred

Runtime integration with external AI providers is out of scope for this MVP. The PriorityAdvisor is intentionally local, deterministic, and usable without credentials or paid API calls.

If external AI integration is explored in a future version, it should be optional and should include credential management, timeout handling, error handling, and a local deterministic fallback. This project does not introduce provider variables or runtime AI behavior.

## Environment Variables

The application reads environment variables from the operating system. `.env.example` is reference documentation only, and the project does not use `python-dotenv`.
