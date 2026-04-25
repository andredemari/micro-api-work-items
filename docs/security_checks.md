# Security Checks

This document describes the deterministic safety gate used before commits, pushes, packaging, or publication.

The checker is intentionally small, local, and non-destructive. It does not use AI, semantic inference, network calls, cleanup automation, history rewriting, or auto-fixes.

## Commands

Run the default release-oriented check:

```powershell
python scripts/safety_check.py
```

Or use the Makefile target:

```powershell
make safety-check
```

Available modes:

```powershell
python scripts/safety_check.py --mode working-tree
python scripts/safety_check.py --mode staged
python scripts/safety_check.py --mode history
python scripts/safety_check.py --mode release
```

The default mode is `release`.

## What The Checker Does

The safety checker fails on:

- tracked or staged private-path patterns defined in `scripts/safety_policy.json`;
- tracked local artifacts such as database files, environment files, ZIP files, Python caches, or pytest caches;
- known incident paths appearing in Git history;
- forbidden public references in public documentation scopes;
- high-confidence structured secret patterns;
- runtime external provider indicators in runtime scopes;
- provider registry, vendor provider, or external provider runtime files added without explicit approval.

The checker warns on:

- suspicious private paths that exist locally but are not tracked or staged;
- raw SQL indicators in runtime code;
- release reminders before publication.

## Output Safety

Findings include detector ID, path, line number when available, and a short message.

Secret findings must not print raw detected values. If a value is included at all, it must be masked or redacted.

## Scope Rules

Runtime provider guardrails apply to runtime scopes such as:

- `app/`;
- `requirements.txt`;
- `.env.example`;
- future runtime configuration files.

Documentation may discuss optional future providers as planning material. Such references should remain future-oriented and must not imply implemented runtime behavior.

## Git Hooks

Hooks are optional and local. Install them only when desired:

```powershell
python scripts/install_git_hooks.py
```

The installer refuses to overwrite existing hooks unless it is run with an explicit force option after human review.

Suggested hook behavior:

- pre-commit: `python scripts/safety_check.py --mode staged`;
- pre-push: `python scripts/safety_check.py --mode release`.

## Non-Destructive Guarantees

The checker must never:

- delete files;
- run `git rm`;
- run history rewrite tools;
- auto-fix files;
- stage files;
- commit changes;
- install hooks automatically.

## Prompt, Data, And SQL Containment

Models and agents must not directly mutate persistent state. Persistent changes must pass through deterministic application services, schema validation, policy checks, audit, and human approval when required.

Local models reduce external data sharing, but they do not remove prompt injection, jailbreak, tool misuse, or data leakage risks. Future model or tool access must be reviewed against allowed tasks, allowed data classes, model version, tests, and review date.

Raw SQL indicators are warning-only in this project. SQLAlchemy ORM usage remains allowed.
