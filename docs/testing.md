# Testing

This guide separates current execution instructions from preserved experiment snapshots. The API's production code is unchanged; testing skills are authoring aids, not runtime API features.

## Contents
- [Quick execution](#quick-execution)
- [Levels and organization](#levels-and-organization)
- [Project profile](#project-profile)
- [Five reusable skills](#five-reusable-skills)
- [Current skill evaluation](#current-skill-evaluation--2026-10-26)
- [Historical experiments](#historical-experiments)
- [Limits](#limits)
- [Sources and attribution](#sources-and-attribution)

## Quick execution

From the repository root, use the existing project Python environment with dependencies installed. No AI-provider credential is needed by the tests.

```text
python -B -m pytest -q -p no:cacheprovider
python -B -m pytest tests/unit -q -p no:cacheprovider
python -B -m pytest tests/integration -q -p no:cacheprovider
python -B -m pytest tests/system -q -p no:cacheprovider
```

Default regression selects unit, integration and system. Characterizations are deliberately separate:

```text
python -B -m pytest tests/characterization -q -p no:cacheprovider
```

An observation capture is not approval of the observed classifier/security/repetition behavior. Explicit paths override default `testpaths`; do not add observation counts to regression approvals.

On Windows, use a **new exclusive** temporary directory per run; pytest may clear the directory passed to `--basetemp`. Interactive Anaconda Prompt/CMD:

```bat
for /f %I in ('python -c "import uuid; print(uuid.uuid4().hex)"') do set "WORKITEMS_TEST_TMP=%TEMP%\work-items-pytest-%I"
python -B -m pytest -q -p no:cacheprovider --basetemp "%WORKITEMS_TEST_TMP%"
```

A batch file needs `%%I`. If temporary Git repositories hit a path-length error, select a shorter authorized parent that already exists and generate a new child path; do not change Git/Windows settings or reuse somebody else's directory. [Other CMD examples](api_examples.md#pytest-temporary-directory-permission-error-in-cmd).

### Optional coverage

Coverage.py is declared in `requirements-dev.txt`; ordinary tests do not require it. Do not install tools implicitly. Set `COVERAGE_FILE` to an authorized path outside the checkout using the selected shell, then measure only the intended source and case selection:

```text
python -B -m coverage run --branch --source=app -m pytest tests/unit tests/integration -q -p no:cacheprovider --basetemp <new-exclusive-directory>
python -B -m coverage report -m
python -B -m coverage json -o <authorized-report-path>
```

Replace placeholders; do not paste them literally. CMD uses `set "NAME=value"`; PowerShell uses `$env:NAME='value'`. Parent coverage does not instrument the separate HTTP children. Report statements and branch destinations, command, source revision/digests and selected cases; Coverage.py JSON alone does not carry all that provenance.

## Levels and organization

| Location | Boundary / reason to keep it |
| --- | --- |
| `tests/unit/` | Deterministic provider decisions and isolated directory/hook helpers |
| `tests/integration/` | Real FastAPI/Pydantic/service/SQLAlchemy/SQLite, service/provider or Git/filesystem/subprocess boundaries |
| `tests/system/` | Owned separate application process over loopback HTTP, including normal restart |
| `tests/characterization/` | Explicit observations, not normative policy acceptance; cases still have a unit or system boundary |
| `tests/conftest.py` | Shared isolated database, observation recorder and process fixture |
| `tests/http_process_support.py` | Shared owned-process launcher used by system and HTTP observation tests |

No existing test file was moved in the skill-portability revision. The level-based layout already describes the boundaries; moving the shared launcher would add import/entry-point churn without a demonstrated benefit. The guide supplies navigation instead. Mapping against the published baseline is identity for existing paths.

Level, technique and purpose differ: `unit/integration/system` are levels, `functional/structural` are selection techniques, `api/tooling` are themes, and `smoke/regression` describe purpose. The in-process health check is integration smoke, not a deployed-system test. The pyramid guides useful boundaries, not a required numerical ratio.

## Project profile

Use this section as task input to the reusable skills. Another project must supply its own contract, fixtures and environment rather than inherit these API rules.

| Input | This checkout |
| --- | --- |
| Runtime / tools | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy, SQLite, pytest, Uvicorn and HTTPX; optional installed Coverage.py |
| Contract sources | [Schemas](../app/schemas/work_items.py), [API examples](api_examples.md), [scope](mvp_scope.md), [local provider](../app/providers/priority/local_provider.py) |
| Functional boundary | Create/read preserve JSON metadata; PATCH changes supplied fields and preserves omitted fields; valid explicit empty string/list/dict values are distinct from omission |
| Validation | Titles 1..200 inclusive; invalid bodies/queries give localized 422 without writing; missing IDs give 404 without modifying unrelated rows |
| Filtering | Optional scalar status/priority enums, AND when combined, ascending ID order over committed current values |
| Classification | Local deterministic suggestions, no stored-item access or persistence side effect; precedence/substring policies remain observations where not specified |
| Pending policy | Explicit PATCH `null` is not silently treated as omission or assigned a new rejection/storage policy |
| Fixtures | `client` and `db_session` each reset the in-memory test engine; do not combine them in one test. A fresh session proves a new identity map, not a different physical connection |
| Tooling | Temporary Git repositories; no installation or modification of this checkout's hooks |
| HTTP support | `tests/http_process_support.py`, installed interpreter, copied app source, exclusive synthetic SQLite, retained `127.0.0.1:0` socket |
| Readiness and limits | Exact `/health` status/body plus PID/source/DB ownership; readiness 15s, requests 5s, normal stop 10s, child lifetime 90s |
| Evidence | JUnit/coverage/logs outside the public tree; optional `EXTENSION_EVIDENCE` overrides observation destination, otherwise fixture temp is used |
| Optional time guard | `HTTP_TEST_WINDOW_FILE` is only used when explicitly supplied by a task; old windows are not reusable authorization |

The root fixture imports app/database modules even for unit-only selection; a unit marker does not claim a fully decoupled runner environment. File-backed tests replace engines/session factories before lifespan and dispose their temporary engines. HTTP children configure storage before imports, ignore proxy environment settings and verify source origins.

For a restart, confirm normal exit before starting another process on the same synthetic file; compare complete committed records. Acquisition and cleanup are protected, and an unconfirmed live handle is retained. Release checks cover the owned port and database file. No existing user server/database is used.

## Five reusable skills

The canonical source is `.agents/skills`. No client-specific copies, global installation or loader configuration are added.

| Skill | Current version | Task / boundary |
| --- | --- | --- |
| [api-integration-functional](../.agents/skills/api-integration-functional/SKILL.md) | 2.0.1 | Contracts, partitions, boundaries and response/storage oracles |
| [api-integration-structural](../.agents/skills/api-integration-structural/SKILL.md) | 2.0.0 | Actual measured gaps, fixed denominator and contract-derived expectations |
| [test-oracle-review](../.agents/skills/test-oracle-review/SKILL.md) | 2.0.0 | First decisive assertions, expected-value sources and justified overlap |
| [bounded-mutation-evaluation](../.agents/skills/bounded-mutation-evaluation/SKILL.md) | 2.0.0 | Pristine controls, one supplied fault per isolated copy and survivor/error interpretation |
| [http-system-lifecycle](../.agents/skills/http-system-lifecycle/SKILL.md) | 2.0.0 | Owned acquisition, readiness, HTTP operations, normal restart and release |

Each skill carries its essential method, prerequisites, outputs, stops and illustrative Python/Pytest example. Design-only work does not need execution permissions. Execution requires the actual profile and authorized capabilities. No skill grants privileges.

Open this repository root in a client with the documented loader. For explicit evaluation, name the skill and verify the actual file read. If its catalog entry is absent, report that; a task-authorized direct path read is not proof of discovery.

See [portability by client/capability](skills_portability.md) for documented discovery and invocation differences. `$name`, `/name` and `skill({name})` are not interchangeable commands. Naming a skill is not proof of native discovery: record catalog availability, actual file read/version/hash, application, result and limitation separately.

## Current skill evaluation — 2026-10-26

This is a new evaluation on published base `1161086305402102dbeada7c966ceb47c7da830e`, not a rerun or rewrite of the historical A/B experiments. Initial valid regression: 193 cases. Evaluation requests are identified in [the prompt record](prompts.md#revised-skill-evaluation-requests).

| Skill/task | Observed contribution / limitation |
| --- | --- |
| Functional | Proposed a distinct explicit-empty PATCH partition; one new integration case added after contract/oracle review, then executed. One instruction refinement clarified design-only prerequisites (2.0.0 -> 2.0.1) |
| Structural | Current parent measurement before the new case: 191 cases, 258/258 statements, 38/38 destinations; no justified coverage-selected addition. A provenance companion was supplied after the reviewer identified missing revision/command/case metadata |
| Oracle review | Canonical JSON strengthens GET/PATCH response typing; complete creation fields/defaults/ID/timestamps now validated before system baselines. Static findings were not original production bugs |
| Bounded mutation | Known no-close operator only; two control cases pass, two mutated cases fail at the close-call assertion. Later pool checks are not reached; no broad mutation score |
| HTTP lifecycle | The two existing system scenarios pass after strengthening their initial object oracle; the focal task's three owned servers exited normally with port/file release |

The new case is `tests/integration/test_work_items_contract.py::test_explicit_empty_patch_values_are_persisted_and_listed`. The typed response check strengthens the existing metadata/PATCH test; `_assert_created` strengthens the two existing HTTP scenarios before their consistency comparisons.

The five task requests explicitly named a skill. Three fresh read-only auxiliary contexts performed functional/structural/oracle analysis; the integrating conversation alone wrote files and executed checks, including mutation and HTTP tasks. The three reviewing agents reported their requested skills absent from preexisting catalogs; mutation/HTTP also used explicit path reads. Native discovery was not tested. Functional 2.0.1 was explicitly reread; catalog reload was not tested. Public historical text was exposed during some reads, so the contexts were not blinded or independent.

Current checks: 194 cases passed (96 functions: unit 8/10, integration 86/182, system 2/2). The 12 characterization cases were collected only, not executed again. Historical 193-case regression and 12 characterization captures remain separate. No observation was promoted to a desired conflict/auth/idempotency contract. All existing case identities/parametrizations are retained; stronger assertions affect three existing test functions and a single new case is justified by the explicit-empty partition.

Preparation failures were preserved: missing temporary parent, private logging/argument handling and LF/CRLF operator matching. The first mutation attempt stopped before applying the operator; it is not a detection. JUnit omitted a failure `type` attribute; final classification used failure-element presence and the actual assertion trace, without rerunning tests for that parsing correction.

## Historical experiments

The following retained snapshots describe their dated stages. Current instructions above take precedence for running the present tree; current skill revisions must not be credited with historical results.


### Functional case traceability

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


### Structural case traceability

| Original measured gap | Contract and observable oracle | Test |
| --- | --- | --- |
| `database.py` no-file/memory return paths | No directory creation; URL parsing does not open a database | `unit/test_database_directory_decisions.py::test_directory_helper_skips_urls_without_a_sqlite_file` |
| `database.py` file-parent path | Actual temporary parent exists; a second call preserves a sentinel | `integration/test_database_lifecycle.py::test_file_sqlite_setup_creates_parent_and_preserves_existing_files` |
| `init_db` and application lifespan | Empty temporary engine gains schema and stores a synthetic record; engine/session factory replaced before lifespan entry | `integration/test_database_lifecycle.py::test_application_lifespan_creates_usable_isolated_schema` |
| `get_db` cleanup | Success/error consumers call close and release the real pooled connection; subsequent checkout succeeds | `integration/test_database_lifecycle.py::test_request_session_closes_and_releases_connection` |

These file-backed SQLite tests use a per-test temporary engine, restore monkeypatched globals, and dispose the engine. They do not use the application's data file. The cleanup consumer is synthetic and in-process; it does not demonstrate business rollback, permissions, another database backend, a deployed service or recovery after process failure.

### Verification snapshot — 2026-10-24

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


### Extension traceability — 2026-10-25

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


## Limits

- Passing tests/100% measured app coverage do not establish absence of defects, general oracle strength or causal superiority of prompts/skills.
- The measured parent selection excludes HTTP system cases; no child-process instrumentation was added.
- Normal restart is not crash recovery or power-loss durability. Ordered client edits are not simultaneous collaboration or authenticated identities.
- The twelve historical observations record stale overwrite, anonymous access and repeated-create duplication, not approved desired policies. No new observation run was needed for this revision.
- Timestamp checks permitting equality do not prove a strict "changed on every update" guarantee; no stronger clock policy or sleeps were introduced.
- The existing Starlette/httpx deprecation warning remains; dependencies were not changed to hide it.
- The safety checker does not inspect new untracked file contents in its normal tracked scan. New public files need explicit review before staging; this is not a scanner certification.
- No other client/model/OS was executed or installed. Local source availability does not make inference offline or enforce sandbox permissions.
- Detailed prompts, raw logs, source hashes, review findings and cleanup records stay outside the public tree. No private project context is required to use these skills.

## Sources and attribution

The Python methods adapt closed-box-test-generation and open-box-test-generation from [aurimrv/go-face-recognition at revision 6c4b8a558a72e4b69edf56394854aefc17769c27](https://github.com/aurimrv/go-face-recognition/tree/6c4b8a558a72e4b69edf56394854aefc17769c27/.cursor/skills). Its [MIT license](https://github.com/aurimrv/go-face-recognition/blob/6c4b8a558a72e4b69edf56394854aefc17769c27/LICENSE) credits copyright (c) 2024 André Oliveira Silva. The initial consultation used main on 2026-10-24; source/license were rechecked on 2026-10-25 at that revision. The later check does not establish the exact initial revision.

A later preserved partial reference collection used [aurimrv/go-face-recognition-unico at the same commit](https://github.com/aurimrv/go-face-recognition-unico/tree/6c4b8a558a72e4b69edf56394854aefc17769c27/.cursor/skills), a distinct repository. It includes eight skills: the two testing selectors, mutation-test-generation, static-analysis-fix and four OpenSpec skills. MIT attribution and the OpenSpec author metadata remain in that reference collection. It is not part of this public tree.

Useful patterns retained: scoped triggers/inputs, partition or measured-gap selection, explicit outputs, pristine mutation controls, report/action separation and closeout verification. Not adopted: Go/cgo/dlib/biometric dependencies, installers, mandatory generated catalogs, OpenSpec's CLI/workflow, automatic 100% loops or open-ended mutation campaigns. The Python instructions are newly written method adaptations; no upstream code or substantial text is copied. The project's Apache-2.0 license is unchanged.

The common format follows the [Agent Skills specification](https://agentskills.io/specification); the headings are local presentation conventions. Optional provider-specific metadata is not a universal requirement. [Official Codex documentation](https://developers.openai.com/codex/skills/) and the other current client sources are linked in the [portability matrix](skills_portability.md). Essential workflows are local; external sources are attribution or optional reading.

Coverage.py 7.17.0 is Apache-2.0 and was already installed in the development environment. No dependency was installed in this revision. The skillguard scanner was unavailable; format validation and a manual pre-use instruction/provenance/permission review were performed. Neither these checks nor written guardrails certify safety.
