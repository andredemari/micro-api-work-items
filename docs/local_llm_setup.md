# Local LLM Setup Guidance

## Purpose

The current MVP works fully offline with the local deterministic PriorityAdvisor and local priority provider. No local LLM, external LLM, network service, API key, model download, or provider configuration is required to run the API or the test suite.

This document is a future-oriented setup guide for users who want to experiment with a local LLM on their own machine. It does not describe current runtime behavior in the app, and it does not add an Ollama provider to the project.

## Recommended Local LLM Path

Ollama is the recommended beginner-friendly local runtime for future experiments because it provides a local command-line workflow and a local HTTP API.

Models are managed outside this repository. Do not commit model files, downloaded model data, caches, or generated artifacts to Git.

Useful official references:

- Ollama documentation: https://docs.ollama.com/
- Ollama API introduction: https://docs.ollama.com/api
- Ollama generate endpoint: https://docs.ollama.com/api/generate

## Minimal Setup Steps

1. Install Ollama from the official download page or your operating system's supported package path.
2. Choose a small local model from the Ollama model library.
3. Pull or run the model locally:

```bash
ollama pull <model-name>
```

or:

```bash
ollama run <model-name>
```

4. Verify that the model is available:

```bash
ollama list
```

5. Verify the local API with curl:

```bash
curl http://localhost:11434/api/generate \
  -d '{"model":"<model-name>","prompt":"Return the word ok.","stream":false}'
```

6. Verify the local API with Windows PowerShell:

```powershell
$body = @{
  model = "<model-name>"
  prompt = "Return the word ok."
  stream = $false
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://localhost:11434/api/generate" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

The default local Ollama API base URL is `http://localhost:11434/api`. The current MVP does not call this URL.

## Practical Hardware Guidance

Start with a small or medium local model suitable for quick local testing. Very large models may require substantial memory, storage, and GPU resources.

GPU VRAM affects model performance, usable context length, and response latency. Ollama may choose defaults based on available hardware and model configuration. Treat this as practical guidance, not a guarantee of performance.

For this project, short prompts and short outputs are enough for a future PriorityAdvisor experiment. There is no need to start with a large general-purpose model.

## Suggested Baseline For This Project

The current app does not use these settings. They are future-only planning notes for a possible optional local provider:

| Setting | Suggested future baseline |
| --- | --- |
| Provider | `ollama` |
| Base URL | `http://localhost:11434` |
| Model | User-selected local model |
| Timeout | Small timeout suitable for local testing |
| Context tokens | Modest context |
| Max output tokens | Short output |

For a simple PriorityAdvisor use case, future prompts should ask for short structured suggestions only. Provider output must be validated before use.

Do not add these settings to runtime code until a separate implementation plan is approved.

## Privacy And Safety Notes

Local LLMs can reduce external data sharing because prompts can stay on the user's machine. Local does not automatically mean safe.

- Do not send secrets, credentials, private data, or sensitive records to any model by default.
- Validate model output against the expected schema before using it.
- Keep the deterministic local provider available as the default fallback.
- Treat LLM output as suggestions, not authoritative decisions.

## Future Integration Plan

A future Ollama provider should be optional and should not affect CRUD behavior.

Future integration requirements:

- Keep the current deterministic local provider as fallback.
- Validate provider output against the existing classification response schema.
- Fall back to deterministic local rules on timeout, connection failure, invalid output, or missing model.
- Keep CRUD endpoints independent from LLM availability.
- Do not allow an LLM to create, update, or delete persisted data without human approval.
- Keep `POST /work-items/classify` side-effect free unless a separate design explicitly changes that contract.

## Explicit Out Of Scope For This Task

- No Ollama provider implementation.
- No OpenAI provider.
- No provider registry.
- No environment variable behavior.
- No new dependencies.
- No `.agent/` folder.
- No API route changes.
- No response format changes.
- No database changes.
