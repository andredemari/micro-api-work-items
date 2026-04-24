# External Provider Planning Guidance

## Purpose

The current runtime remains local deterministic only. The API uses the local PriorityAdvisor and local priority provider, and it does not call external LLM providers.

This document describes how a future optional external provider could be introduced safely. It is planning guidance only. It does not implement provider code, provider registry behavior, credentials, environment variables, dependencies, route changes, schema changes, or response format changes.

Any future implementation requires separate approval.

## Provider-Agnostic Strategy

Future external provider support should be generic rather than tied to a single vendor. A later implementation can evaluate specific vendors, but the project should first define the behavior it needs:

- accept a work item classification input;
- request a short suggestion from an optional provider;
- validate provider output against the existing classification response schema;
- fall back to the deterministic local provider on failure;
- keep the current public API unchanged.

Vendor-specific provider modules should not be added until a separate implementation plan is approved.

## Required Safety Controls

Before any implementation, the plan must address:

- Credential handling: secrets must come from a safe runtime secret mechanism and must never be committed.
- Timeout handling: provider calls must have short bounded timeouts.
- Error handling: connection errors, rate limits, invalid output, and unavailable providers must not break CRUD.
- Local fallback: the deterministic local provider must remain available and must be the default fallback.
- Output validation: external responses must be parsed and validated before use.
- Privacy and data minimization: prompts should include only the minimum fields needed for classification.
- Provider lock-in: interfaces and tests should avoid depending on vendor-specific response shapes.

## Runtime Behavior Rules

Future external provider use must be optional.

- CRUD endpoints must never depend on LLM availability.
- `POST /work-items/classify` must remain side-effect free unless a separate design explicitly changes that contract.
- No LLM should create, update, or delete persisted data without human approval.
- Provider failure must return a deterministic local suggestion or a clearly handled fallback result.
- Missing credentials or missing provider configuration must not prevent the app from starting.

## Future Configuration Notes

No environment variables are added in this planning task.

If a future implementation needs configuration, it should be planned separately and should clearly distinguish:

- provider selection;
- provider base URL;
- model name;
- timeout;
- maximum output length;
- credential reference.

Configuration names and `.env.example` placeholders should not be introduced until runtime behavior is approved.

## Testing Strategy

Future tests must use mocks, fakes, or local deterministic logic only.

- No real network calls should be required in tests.
- No paid API calls should be required in tests.
- Provider timeout, invalid output, and fallback behavior should be tested with fakes.
- Existing API tests should continue to prove public response shape and non-persistence behavior.
- Local provider tests should remain the baseline for deterministic output.

## Future Implementation Checklist

Before implementation, require a separate plan covering:

- exact provider abstraction shape;
- provider selection rules;
- timeout and retry policy;
- fallback behavior;
- output schema validation;
- secret handling;
- mock-only test strategy;
- documentation updates;
- acceptance criteria proving public API behavior remains unchanged.

## Explicit Out Of Scope

- No external provider implementation.
- No provider registry.
- No vendor-specific provider files.
- No OpenAI, Anthropic, Gemini, Groq, OpenRouter, or other provider integration.
- No credentials.
- No environment variable behavior.
- No `.env.example` changes.
- No dependencies.
- No API route changes.
- No response format changes.
- No schema changes.
- No database model changes.
- No `.agent/` folder.
- No tag or release.
