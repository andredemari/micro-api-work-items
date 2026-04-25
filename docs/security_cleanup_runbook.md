# Security Cleanup Runbook

Use this runbook when private files, credentials, local artifacts, database files, or sensitive planning documents are accidentally added to Git.

## Stop Condition

Pause roadmap work immediately. Do not publish, push, tag, release, or continue feature work until the cleanup is complete and reviewed.

If credentials or secrets are involved, assume they may be compromised and plan rotation before any publication.

## Initial Audit

Identify the current repository state and the affected path without printing sensitive contents:

```powershell
git status --short
git remote -v
git log --all -- <path>
git ls-files <path>
git grep -n "<safe-pattern>"
```

Use targeted path and name patterns. Avoid displaying file contents when the file may contain private or sensitive material.

## Important Git Behavior

`.gitignore` prevents future accidental additions of untracked files. It does not remove files that are already tracked, and it does not remove files from Git history.

If a sensitive file was committed, deleting it in a later commit is not enough for a public repository. The historical blob can still remain reachable from earlier commits until history is rewritten and old objects are pruned.

## Decision Tree

### Not Pushed Or Published

If the repository has not been pushed to any public or shared remote:

1. Create a private local backup.
2. Rewrite local history with an approved tool such as `git-filter-repo`.
3. Remove public references to the sensitive file or wording.
4. Add ignore rules for the sensitive path or file pattern.
5. Verify that the path is no longer tracked or present in history.
6. Prune unreachable objects after validation.

### Pushed To A Private Remote

If the repository was pushed to a private remote:

1. Pause collaboration and notify affected maintainers.
2. Rotate credentials if secrets were involved.
3. Rewrite local history only with explicit human approval.
4. Coordinate a force-push plan with collaborators.
5. Ensure other clones are recloned or cleaned.

### Pushed To A Public Remote

If the repository was pushed publicly:

1. Treat credentials as exposed and rotate them immediately.
2. Remove or restrict public access if possible.
3. Follow the hosting provider's sensitive-data removal guidance.
4. Rewrite history only with explicit human approval.
5. Communicate that old forks, clones, and caches may still contain the data.

## Backup Before History Rewrite

Before a destructive rewrite, create a private local backup bundle outside the repository:

```powershell
git bundle create ..\repo-before-cleanup.bundle --all
git rev-parse HEAD
```

The backup may contain the sensitive material. Keep it private, store it securely, or delete it after validation if it is no longer needed.

## History Rewrite

Use `git-filter-repo` for history cleanup when a committed path must be removed from all history:

```powershell
git filter-repo --path <path> --invert-paths --force
```

Only run destructive history rewrites with explicit human approval. Do not use manual rewrite commands unless the cleanup plan specifically approves them.

## Cleanup Public References

After rewriting history, search current tracked files for public references:

```powershell
git grep -n "<path-or-safe-pattern>"
```

Remove or generalize public references as needed. Add ignore rules for local-only paths and file patterns.

## Verification

Verify the sensitive path is gone from history and tracking:

```powershell
git status --short
git log --all -- <path>
git ls-files <path>
git grep -n "<path-or-safe-pattern>"
python scripts/safety_check.py
python -m pytest -q
git ls-files | Select-String -Pattern "\.db$|\.sqlite$|\.sqlite3$|__pycache__|\.env$|\.pytest_cache|\.zip$"
```

Expected results:

- The sensitive path is absent from `git log --all -- <path>`.
- The sensitive path is absent from `git ls-files <path>`.
- Only intentional ignore rules remain.
- The deterministic safety checker passes.
- Tests pass.
- The working tree is clean.
- No local artifacts are tracked.

## Prune Old Objects

After verification, expire reflogs and prune unreachable objects:

```powershell
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

Verify again after pruning:

```powershell
git log --all -- <path>
git ls-files <path>
git status --short
```

## Credential Rotation

If credentials, tokens, API keys, passwords, private URLs, or signing material were committed, rotate them even if history was rewritten. History cleanup reduces repository exposure, but it does not prove a credential was never copied.
