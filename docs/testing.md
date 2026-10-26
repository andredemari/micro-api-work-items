# Testing

## Levels and selection

`tests/unit/` exercises isolated deterministic provider behavior and a pure hook helper. `tests/integration/` crosses real boundaries: in-process FastAPI/Pydantic/service/SQLAlchemy/SQLite, service/provider, or Git/filesystem/subprocess tooling. The health check is an in-process integration smoke check, not a deployed system test. `tests/system/` exercises an owned HTTP process and normal restart with exclusive synthetic SQLite.

Level markers are `unit`, `integration` and `system`. `api` and `tooling` are themes; `smoke` is a purpose. Functional and structural describe case-selection techniques, not levels. The existing suite is also used for regression. The test pyramid guides where an assertion belongs without imposing proportions or removing useful integrations.

## Running tests

From the repository root with the existing project interpreter:

```text
python -B -m pytest -q -p no:cacheprovider
python -B -m pytest -q -m unit -p no:cacheprovider
python -B -m pytest -q -m integration -p no:cacheprovider
```

Tests set `DATABASE_URL` to in-memory SQLite before importing the app. The shared fixtures recreate tables per test and override request database sessions. Do not combine `client` and `db_session` fixtures in one test: each resets the shared test engine. Tooling tests use temporary Git repositories, not this checkout's hooks.

If Windows temporary-directory cleanup fails, select a **new, exclusive** directory for each run; pytest may clean the supplied directory. Anaconda Prompt/CMD:

```bat
for /f %I in ('python -c "import uuid; print(uuid.uuid4().hex)"') do set "WORKITEMS_TEST_TMP=%TEMP%\work-items-pytest-%I"
python -B -m pytest -q -p no:cacheprovider --basetemp "%WORKITEMS_TEST_TMP%"
```

These are interactive CMD commands; a batch file needs `%%I`. A fresh SQLAlchemy session proves a different identity map and committed visibility on the test engine, not independent physical connections or process restart. TestClient does not demonstrate real network, deployment or multiple identities.

## Coverage

Coverage is optional for ordinary tests. Install `requirements-dev.txt` only in the intended development environment. Keep data/reports outside the checkout; for example set `COVERAGE_FILE` to a private absolute path, then run:

```text
python -B -m coverage run --branch --source=app -m pytest -q -p no:cacheprovider
python -B -m coverage report -m
```

Report executed statements and branch destinations separately. A high percentage is not proof of a strong oracle. Do not change production or impose a 100% target to improve the number.

## Contracts and candidate selection

Use the schemas, [API examples](api_examples.md), [scope](mvp_scope.md) and [local provider](../app/providers/priority/local_provider.py) together. Relevant observable contracts: create/read preserve JSON metadata; PATCH preserves omitted fields; deletion makes the item unavailable; status/priority filters combine by AND over committed current values; classification is deterministic and does not alter stored items; titles have length 1 through 200 inclusive. Invalid requests return field-localized 422 errors without writing. Missing IDs return 404 without changing other records.

Explicit `null` in PATCH remains a contract question: optional schema annotations alone do not establish a storage policy. It is not silently treated as omission, rejected, or fixed by these tests.

## Repo-local skills

The two original instruction-only skills live in `.agents/skills/`: `api-integration-functional` starts from contracts and partitions; `api-integration-structural` starts from actual baseline line/branch gaps while retaining contract-derived oracles. Three complementary skills cover oracle review, bounded mutation evaluation and owned HTTP process lifecycle, as described under Skills and source boundaries below. Launch Codex in this checkout so repo-local discovery can apply. Explicitly mention the skill in the host's supported selector (`$skill-name` in Codex CLI/IDE). Merely creating the files or passing pytest does not demonstrate discovery or correct invocation. Never copy them to user-global locations to hide a discovery failure.

## Method origins

The Python workflows adapt the **method**, not the commands, of [closed-box-test-generation](https://github.com/aurimrv/go-face-recognition/blob/6c4b8a558a72e4b69edf56394854aefc17769c27/.cursor/skills/closed-box-test-generation/SKILL.md) and [open-box-test-generation](https://github.com/aurimrv/go-face-recognition/blob/6c4b8a558a72e4b69edf56394854aefc17769c27/.cursor/skills/open-box-test-generation/SKILL.md), in aurimrv/go-face-recognition. The upstream [MIT license](https://github.com/aurimrv/go-face-recognition/blob/6c4b8a558a72e4b69edf56394854aefc17769c27/LICENSE) credits copyright (c) 2024 André Oliveira Silva. The initial consultation used main on 2026-10-24; source and license were rechecked on 2026-10-25 at revision `6c4b8a558a72e4b69edf56394854aefc17769c27`. That later check does not establish the exact revision read during the initial consultation. These are newly written Python instructions adapting the method, with no upstream code or substantial text copied. This repository's Apache-2.0 license remains unchanged.

Retained: contract partitions/boundaries, measured structural gaps, traceability and critical review. Not inherited: Go/cgo/dlib commands, generated catalog files, automatic installs, or a default whole-project 100% loop. [Official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills) describes repo-local discovery. Coverage.py 7.17.0 is Apache-2.0. Mutation testing was not executed in the initial 2026-10-24 milestone. The later bounded reproduction is described in the extension verification snapshot below; it is not a new discovery or a general mutation score.


## Functional case traceability

| Group | Contract and selection criterion | Test in `tests/integration/test_work_items_contract.py` |
| --- | --- | --- |
| JSON-PATCH | Nested JSON round-trip; omitted PATCH fields retained in committed rows | `test_nested_metadata_roundtrip_and_omitted_patch_fields` |
| FILTER-PATCH | Updated values change membership; old/new AND queries and unaffected record | `test_filters_use_values_after_committed_patch` |
| CLASSIFY-EXISTING | Suggestions do not modify a preexisting row, including timestamps | `test_classification_preserves_preexisting_record` |
| TITLE | POST/PATCH lengths 0, 1, 2, 199, 200, 201; valid/invalid partitions | `test_title_boundaries` |
| INVALID-BODY | Invalid enum, tag-member and metadata-container partitions; localized error, no write | `test_invalid_body_is_localized_and_does_not_write` |
| REQUIRED-TITLE | Missing and null title on create; not a PATCH-null policy | `test_create_requires_non_null_title_without_writing` |
| MISSING-ID | GET/PATCH/DELETE absent ID preserve an unrelated existing row | `test_missing_id_preserves_unrelated_item` |

Additional static filter combinations, query errors, another determinism-only check and the already-tested delete response shape were not duplicated. Repeated requirements are justified only where the new assertion checks a distinct persisted effect. Root `conftest.py` still imports application/database dependencies even for unit-only selection; the level describes the test boundary, not a fully decoupled test-runner environment.


## Structural case traceability

| Original measured gap | Contract and observable oracle | Test |
| --- | --- | --- |
| `database.py` no-file/memory return paths | No directory creation; URL parsing does not open a database | `unit/test_database_directory_decisions.py::test_directory_helper_skips_urls_without_a_sqlite_file` |
| `database.py` file-parent path | Actual temporary parent exists; a second call preserves a sentinel | `integration/test_database_lifecycle.py::test_file_sqlite_setup_creates_parent_and_preserves_existing_files` |
| `init_db` and application lifespan | Empty temporary engine gains schema and stores a synthetic record; engine/session factory replaced before lifespan entry | `integration/test_database_lifecycle.py::test_application_lifespan_creates_usable_isolated_schema` |
| `get_db` cleanup | Success/error consumers call close and release the real pooled connection; subsequent checkout succeeds | `integration/test_database_lifecycle.py::test_request_session_closes_and_releases_connection` |

These file-backed SQLite tests use a per-test temporary engine, restore monkeypatched globals, and dispose the engine. They do not use the application's data file. The cleanup consumer is synthetic and in-process; it does not demonstrate business rollback, permissions, another database backend, a deployed service or recovery after process failure.

## Verification snapshot — 2026-10-24

Python 3.11.17, pytest 9.1.1, Coverage.py 7.17.0 on Windows. Production was unchanged from baseline `3c74cc9`. Cases are parametrized pytest items; functions are source definitions.

| Stage | Unit functions / cases | Integration functions / cases | Total functions / cases |
| --- | --- | --- | --- |
| Baseline before moves | 5 / 5 | 73 / 143 | 78 / 148 |
| Reorganized, no new cases | 5 / 5 | 73 / 143 | 78 / 148 |
| Reviewed union | 6 / 8 | 83 / 179 | 89 / 187 |

Reorganization preserved all 78 test bodies and parameter decorators by AST comparison, mapped all 148 collection IDs, and retained the shared fixtures. A move is not a new test or a new level. The integration-heavy distribution is descriptive, not a pyramid target or a reason to remove useful checks.

| Comparable set | Passed cases | Executed statements | Executed branch destinations |
| --- | --- | --- | --- |
| Baseline | 148 | 248/258 (96.12%) | 36/38 (94.74%) |
| Baseline + contract-led A | 180 | 248/258 (96.12%) | 36/38 (94.74%) |
| Baseline + coverage-led B | 155 | 258/258 (100%) | 38/38 (100%) |
| Reviewed union | 187 | 258/258 (100%) | 38/38 (100%) |

Each set ran in a fresh process with the same explicit baseline files, unchanged production, `--branch --source=app`, disabled pytest cache and an exclusive temporary directory. Only the selected A/B files differed. A's stronger content/state oracles did not increase coverage. B reached all measured app statements/destinations; this is a measurement of this scope, not proof of correctness. Mutation and deployed/network tests were not performed.

A (32 cases) and B (7 cases) each passed their first targeted run; no corrective refinement was needed. Full regression was repeated without coverage: 187 passed. One existing Starlette/httpx deprecation warning remains; dependencies were not updated to hide it. The sequential Codex session reported both skills in its catalog and explicitly read each SKILL.md; this evidence does not establish implicit matching reliability or superiority caused by the prompt. The session retained prior context, so the comparison was not independent or blinded.

Safety checker source was unchanged. Its normal check does not inspect the contents of new untracked files; those require explicit review before staging/publication. Scanner output alone does not establish information safety. Execution logs and raw coverage data are not part of the public tree.


## Incremental testing practices

The prior verification snapshot above remains a separate milestone. The extension preserves its cases and adds risk-led checks without a test-count or coverage target. New public material uses technical names; detailed execution/evaluation logs remain outside this repository.

### Traceability and oracle status

For each case record: source/requirement -> **defined contract**, **observed behavior** or **pending decision** -> partition/boundary/branch or risk -> stable case ID/test -> actual result/run -> skill version/hash. A branch executed is not an assertion verified. Observed classifier precedence and HTTP limitations are not silently promoted to desired contracts.

| ID | Status and source | Property / selected test |
| --- | --- | --- |
| CLS-INPUT | Side-effect invariant, local suggestion boundary | Input model/tags preserved by `test_classification_preserves_input_model_and_tags` |
| CLS-ALIAS | Side-effect invariant, local suggestion boundary | Modifying returned tags/reasons changes neither input nor other results; `test_suggested_tags_do_not_alias_input_or_other_results` |
| OBS-CLS-* | Observed implementation, policy not formalized | Category/priority collisions; isolated term origin; case; tag order/dedup; substring in download. No desired output asserted |
| SYS-JOURNEY | CRUD/validation contracts in schemas and API examples | Real process/HTTP, exact typed JSON, committed values reflected in filters; localized invalid requests preserve both HTTP and read-only SQLite snapshots |
| SYS-RESTART | Local SQLite setup/persistence contract | Complete records survive an orderly stop and a new process on the same synthetic file; not crash qualification |
| OBS-HTTP-CONCURRENCY | Observation, no version-control contract | Two clients read the same state, then update the same field in controlled order; capture responses/final state, no 409 requirement |
| OBS-HTTP-AUTH | Observation, no access-control implementation | Requests without credentials; allowed access is absence of a barrier in this flow, not a security pass |
| OBS-HTTP-REPETITION | Observation, no idempotency implementation | Discard response after confirmed write, query state, deliberately repeat once; record any duplication |
| REP-M2 | Known procedure reproduction | Same no-close operator and148 old/2 selected lifecycle cases; no new discovery or general mutation score |

The regression default selects `tests/unit`, `tests/integration`, and `tests/system`. Run observations explicitly with `python -B -m pytest tests/characterization -q -p no:cacheprovider`, using a fresh exclusive temporary directory. Supplying another directory explicitly overrides pytest's default testpaths; do not combine observation counts with regression approval. A passed observation means capture completed, not the observed policy/security behavior was accepted.

### Owned HTTP test process

`tests/http_process_support.py` snapshots only application source, sets the synthetic database before importing it and launches the existing Python interpreter in isolated mode. It binds and retains an owned 127.0.0.1:0 socket; actual PID, source hashes/origins, health and assigned port are verified. HTTPX ignores proxy environment settings. No reload, external bind, shared runtime database or installed service.

Readiness is bounded to 15s, requests 5s, orderly stop 10s and process lifetime 90s. The test sends a private stdin stop command to its own process; watchdog/forced termination is not a successful normal shutdown. Fixture cleanup runs in finally, records exit/reason, verifies port rebind and database-file release, and preserves logs/synthetic evidence. The helper targets the installed Uvicorn interface; other OS/version support is not established by a Windows run. A loopback test is not a firewall/host-egress isolation proof.

Characterization clients are anonymous client instances, not authenticated users. Ordered writes use completed responses, not random races/sleeps. Discarded responses are simulated in the client after confirmed success, not actual packet loss. Explicit PATCH null remains pending and is not exercised by new policy tests.

### Skills and source boundaries

The two existing skills now carry explicit version metadata; earlier unversioned instructions remain identified by their historical snapshot/hash. `test-oracle-review` reviews assertion quality, `bounded-mutation-evaluation` runs only supplied controlled faults, and `http-system-lifecycle` manages owned process resources. None substitutes for the others or grants execution permission. Each is evaluated on a concrete task, reading/use evidence, ambiguity, rework and human intervention, with at most one motivated refinement and a keep/revise/combine/discard conclusion.

Additional method references: [the eight source skills](https://github.com/aurimrv/go-face-recognition-unico/tree/6c4b8a558a72e4b69edf56394854aefc17769c27/.cursor/skills), revision6c4b8a558a72e4b69edf56394854aefc17769c27, in aurimrv/go-face-recognition-unico (a distinct repository from the earlier linked go-face-recognition, containing that same commit). MIT attribution is preserved; local Python instructions are newly written adaptations, not upstream Go scripts. OpenSpec's four skills remain reference material only. No second governance workflow or runtime dependency was adopted.

No Python linter/type/security analyzer or skillguard executable was available in the checked environment. No new tool was installed. AST parsing, the existing safety checker and manual review are narrower checks, not equivalent analyzers or safety certification. Do not run upstream installers, npx/Go commands or automatic mutation/coverage loops.

Parent-process coverage remains separate from uninstrumented HTTP children. The existing 100% app measurement does not demonstrate that these system scenarios or assertions were covered, nor that skills caused better correctness.


### Extension verification snapshot — 2026-10-25

The 187-case milestone was restored byte-for-byte and revalidated before extension edits. A first recovery run failed in temporary Git object writes because paths were too long; a fresh short temporary root resolved it without changing tests or Git/Windows settings. Failure logs were retained.

| Set | Source functions / parametrized cases | Observed result |
| --- | --- | --- |
| Existing milestone |89 /187 |187 passed in restored copy |
| Unit regression |8 /10 |Preservation/alias invariants added; no classifier-policy contract introduced |
| Integration regression |85 /181 |Includes two simulated executor-failure checks; not live hung-process tests |
| Real HTTP system regression |2 /2 |Journey/invalid-no-write and normal restart on same synthetic SQLite passed |
| Default regression total |95 /193 |193 passed, existing Starlette/httpx warning remains |
| Explicit characterization |4 /12 |12 observation captures completed; not policy/security acceptance |

Final parent-only unit/integration coverage ran 191 cases with --branch --source=app: 258/258 executable statements and 38/38 branch destinations. HTTP children were not instrumented or counted as covered by that report. This repeats the already-saturated app denominator; it is not a coverage-driven quality gain.

Actual HTTP observations: ordered stale writes both returned 200 and the final value came from the second edit; anonymous list/create returned 200/201; reconciliation found one row after the discarded response and explicit repeated POST produced a second ID. These are limitations observed in the synthetic instance, not desired conflict/authentication/idempotency contracts. Download matched the down substring in the current classifier; policy remains undecided.

The known no-close mutation was reproduced using the same 148 old and two lifecycle cases. Controls passed; the mutation survived the old set and failed both new close-call assertions. This was a procedure reproduction, not a newly discovered bug or broad mutation-score result.

Skill conclusions: retain functional and HTTP lifecycle instructions after one motivated refinement each (1.0.1); retain oracle review and bounded mutation instructions (1.0.0) for separate jobs; retain structural instructions conditionally (1.0.0), with limited evidence here because no executable coverage gap remained. Catalog/file-read evidence came from two read-only auxiliary reviews; the integrating conversation applied changes and executed checks. Refined catalog reload and causal superiority were not established.

Six real server processes stopped normally with port/database release and unchanged-source checks, without forced termination. The bounded HTTP window ended early after cleanup. No crash/power-loss, real network-loss, multi-user authorization, external deployment or other-OS qualification was performed. Production, runtime requirements, historical test bodies, README and licensing remained preserved; no dependencies were installed.
