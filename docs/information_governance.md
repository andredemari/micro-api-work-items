# Information Governance

This guide defines public-safe documentation boundaries for this repository.

## Information Classification

| Level | Meaning | Repository handling |
| --- | --- | --- |
| Public | Safe to publish openly. | Allowed in tracked documentation and code. |
| Internal | Useful to maintainers but not intended for publication. | Keep outside the repository when possible. |
| Confidential | Could reveal private plans, strategy, sensitive operations, or non-public context. | Do not commit. |
| Restricted | Credentials, secrets, customer data, sensitive personal data, or regulated information. | Never commit; rotate if exposed. |

## Appropriate Public Content

Public repository content may include:

- generic project goals;
- public API behavior;
- setup and test instructions;
- architecture diagrams;
- technical decisions;
- sanitized prompt examples;
- public-safe limitations and future planning.

## Content That Must Stay Out

Do not commit:

- credentials, tokens, passwords, private keys, or API keys;
- private strategy, private roadmap rationale, or sensitive planning notes;
- customer data or sensitive personal data;
- internal system names, private paths, private URLs, or operational secrets;
- local demo notes or private presentation scripts;
- local database files, cache files, generated archives, or machine-specific artifacts.

## Local Private Working Areas

Keep sensitive material outside the repository when possible. If temporary local notes must exist near the project, use ignored local-only locations such as:

- `.private/`
- `private/`
- `docs/priv/`
- `*.private.md`
- `*.secret.md`
- `*.local.md`

Ignored files are not a security boundary. They reduce accidental commits, but local files can still be copied, backed up, or force-added. Review carefully before publication.

## Governance Principles

- Need-to-know: include only information required for public understanding and reproducibility.
- Data minimization: keep examples generic and avoid private context.
- Human review: inspect documentation and Git status before publishing.
- Separation: keep public docs separate from internal notes and private strategy.
- No sensitive data: never include private strategy, credentials, customer data, or sensitive personal data in public docs.

## Pre-Publication Review

Before publishing or packaging:

```powershell
git status --short
git grep -n "secret\|token\|password\|credential\|private\|internal"
git ls-files | Select-String -Pattern "\.db$|\.sqlite$|\.sqlite3$|__pycache__|\.env$|\.pytest_cache|\.zip$|\.private/|private/|docs/priv/"
```

Use judgment with search results. Some public-safe governance documents may mention these words while explaining what must not be committed.
