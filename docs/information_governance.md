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

Keep sensitive material outside the repository when possible. If temporary local notes must exist near the project, keep them out of Git and review them before publication.

The deterministic safety checker treats patterns such as these as private-path risks if they are staged or tracked:

- `.private/`
- `private/`
- `docs/priv/`
- `*.private.md`
- `*.secret.md`
- `*.local.md`

These patterns are enforced by `scripts/safety_policy.json` and `scripts/safety_check.py`, not by turning `.gitignore` into a broad policy registry. Ignored files are not a security boundary; local files can still be copied, backed up, or force-added.

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
python scripts/safety_check.py
make safety-check
```

Use the deterministic checker as the main gate. Manual searches may still help during review, but broad keyword searches can produce misleading results because governance documents legitimately mention words such as secret, token, credential, private, and internal.
