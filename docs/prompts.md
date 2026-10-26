# Prompt Traceability

This document records sanitized, representative prompts used to support
academic reproducibility. It is not raw chat history. The prompts are written
to show the kind of AI-assisted work used across planning, implementation,
review, documentation, and final hardening.

## Public-Safe Rules

- Do not include private chat history, private paths, credentials, tokens,
  internal systems, customer data, or private strategy.
- Keep examples generic and course-oriented.
- Preserve the current MVP boundary: local, deterministic, public, and simple.
- Do not introduce runtime external AI providers, local LLM runtime behavior,
  embeddings, RAG, agents, queues, streaming, frontend, authentication,
  external integrations, or `python-dotenv`.

## CO-STAR-Like Shape

The prompts below use a compact CO-STAR-like structure:

- Context: background and constraints.
- Objective: what the assistant should produce.
- Style: implementation or writing expectations.
- Tone: how the response should read.
- Audience: who will review or use the result.
- Response: expected output format.

## Traceability Log

| ID | Phase | Main artifacts | Verification evidence |
| --- | --- | --- | --- |
| P-001 | Scope planning | `docs/mvp_scope.md`, `docs/architecture.md` | MVP scope, out-of-scope list, route plan |
| P-002 | Project setup | `.gitignore`, `requirements.txt`, `Makefile`, `.env.example` | Local setup commands and ignored artifacts |
| P-003 | API implementation | `app/main.py`, `app/controllers/`, `app/schemas/`, `app/services/` | Health, CRUD, validation, and error tests |
| P-004 | Persistence | `app/db/database.py`, `app/models/`, `app/repositories/` | Service and repository tests |
| P-005 | PriorityAdvisor | `app/services/priority_advisor.py`, `app/providers/priority/local_provider.py` | Deterministic classifier and provider tests |
| P-006 | Documentation | `README.md`, `docs/api_examples.md`, `docs/decisions.md` | Reproducible setup, examples, decisions |
| P-007 | Review and safety | `scripts/safety_check.py`, `scripts/safety_policy.json`, `tests/integration/test_safety_check.py`, `tests/unit/test_safety_helpers.py` | Safety-check tests and release gate |
| P-008 | Final course readiness | `docs/course_submission_traceability.md`, `docs/release_checklist.md` | Requirement-to-artifact mapping |

## Representative Sanitized Prompts

### P-001 Scope Planning

- Context: A postgraduate course requires a small task-oriented micro-API.
  The repository must remain public, academic, local, deterministic, and easy
  to run.
- Objective: Plan a FastAPI MVP for generic work items, including endpoints,
  data fields, architecture, tests, documentation, and explicit exclusions.
- Style: Keep the plan incremental and implementation-ready.
- Tone: Direct and reviewer-friendly.
- Audience: Course reviewer and future maintainer.
- Response: MVP scope, acceptance checklist, file layout, and commit sequence.

### P-002 Project Setup

- Context: The project should run locally without external services or paid
  provider credentials.
- Objective: Define Python dependencies, ignored local artifacts, environment
  reference values, and basic Makefile commands.
- Style: Prefer simple commands and Windows-friendly guidance.
- Tone: Practical.
- Audience: Student, reviewer, and anyone reproducing the project.
- Response: `.gitignore`, `requirements.txt`, `.env.example`, and Makefile
  targets for install, run, test, and safety checks.

### P-003 API Implementation

- Context: The API needs health, CRUD, and classification endpoints under the
  work-item vocabulary.
- Objective: Implement FastAPI routes, Pydantic contracts, service functions,
  and HTTP error handling without expanding scope.
- Style: Keep controllers thin and move application behavior into services.
- Tone: Precise and conservative.
- Audience: Maintainer reviewing the code.
- Response: Route handlers, schemas, services, and tests for success and error
  cases.

### P-004 Persistence

- Context: Persistence should be local and inspectable for the MVP.
- Objective: Configure SQLite through SQLAlchemy, isolate database access, and
  make tests independent from the runtime database file.
- Style: Use a small repository layer rather than spreading queries through
  route functions.
- Tone: Engineering-focused.
- Audience: Course reviewer and future maintainer.
- Response: Database setup, SQLAlchemy model, repository functions, and
  repository/service regression tests.

### P-005 PriorityAdvisor

- Context: The course includes the idea of suggesting priority or
  classification, but the current release must not call an external AI
  provider.
- Objective: Represent `PriorityAdvisor` as local deterministic suggestion
  logic that returns type, priority, tags, and reasons.
- Style: Keep the endpoint side-effect free and keep persisted CRUD separate.
- Tone: Clear about boundaries.
- Audience: Reviewer checking whether AI runtime scope was added.
- Response: Local provider rules, PriorityAdvisor service, classification
  endpoint, and tests proving deterministic non-persistence.

### P-006 Documentation

- Context: The repository is intended for public GitHub publication and course
  submission.
- Objective: Explain objective, setup, run commands, endpoints, examples,
  limitations, AI assistance, design decisions, and packaging guidance.
- Style: Keep README concise and move detailed evidence into supporting docs.
- Tone: Public-safe and course-oriented.
- Audience: Course reviewer and public reader.
- Response: README updates, API examples, decision log, traceability document,
  and release checklist.

### P-007 Review And Safety

- Context: Public publication requires checking tracked files, ignored local
  artifacts, provider scope, and accidental sensitive content.
- Objective: Add deterministic repository checks and tests without deleting
  files, rewriting history, staging files, or using AI inference.
- Style: Prefer explicit policy data, redacted findings, and temporary Git
  repositories in tests.
- Tone: Strict and factual.
- Audience: Maintainer preparing a release.
- Response: Safety checker, policy data, safety-check tests, and documentation
  for pre-publication use.

### P-008 Final Course Readiness

- Context: Before tagging, the project needs a clean course-submission story
  and evidence that the MVP remained within scope.
- Objective: Map course expectations to repository artifacts, clarify final
  limitations, and verify public/private boundaries.
- Style: Use a checklist and concise artifact mapping.
- Tone: Evidence-based.
- Audience: Course reviewer.
- Response: Course traceability, release checklist updates, and a short
  pre-publication review summary.


## Reusable Test Requests

These are condensed, sanitized request examples derived from the testing workflow, not verbatim execution transcripts or evidence that a particular host loaded a skill. Historical prompt descriptions above are retained; artifact paths reflect the current test layout. See [the testing guide](testing.md) for levels, isolation and verification limits.

### Contract-Led Request

```text
Use $api-integration-functional. Read the API contract and existing tests.
Before generating cases, define partitions, title boundaries and expected
responses plus stored-state effects. Propose only distinct gains or stronger
oracles; preserve the isolated fixtures. Defer unresolved PATCH null rules.
Run only authorized checks, preserve the initial output and review findings,
and report real results. Do not change production to make tests pass.
```

### Coverage-Led Request

```text
Use $api-integration-structural with the measured baseline and unchanged app
source. Inspect meaningful missing lines and branches, then derive expected
results from contracts. Prefer unit checks for isolated decisions and real
integration checks for resource boundaries. Keep candidate sets separate,
compare over the same denominator, and report remaining gaps and limitations.
Do not assume a 100% goal or install tools without authorization.
```


## Historical A/B requests — 2026-10-24

These are the retained task inputs to the read-only auxiliary design session, not the current 2.x skills. They are reproduced as text below with newline normalization only; no personal filesystem paths occur in them. The integrating conversation subsequently reviewed, wrote and executed the proposals. Original historical skills had no version number and were identified by their preserved hashes.

| Experiment | Inputs and distinct contribution | Initial adjustments |
| --- | --- | --- |
| A, functional | Contracts/partitions/boundaries; 32 integration cases; nested JSON, omitted PATCH fields, post-update filter membership, harmless invalid/missing requests and classification without persistence | Initial cases passed; no corrective refinement. Coverage did not increase |
| B, structural | Original measured gaps; 7 cases: 4 integration and 3 unit; directory decisions, real lifespan/schema and success/error session cleanup | Initial cases passed; no corrective refinement. Measured app denominator reached 258 statements /38 destinations |

A's 32 cases and B's 7 are not counts for the 2.x evaluation. Baseline+A180, baseline+B155 and union187 are historical executed sets. Examples of their distinct oracles and measurement limits remain in [the testing guide](testing.md#historical-experiments). Later skill refinements must not be credited retroactively to A/B.

### A — retained original request

```text
Use $api-integration-functional in this existing academic API checkout. This is a sequential read-only design session; the integrating conversation is the only writer. Do not edit files, run tests or imports, install dependencies, read credentials, create other agents, commit or publish.
First report whether api-integration-functional appeared in the available skill catalog (name/path) and actually read its SKILL.md. Separate automatic discovery from explicit file loading; do not claim discovery merely because this prompt names it. Read applicable instructions, docs/testing.md, docs/api_examples.md, docs/mvp_scope.md, app/schemas/work_items.py and existing tests only as necessary for contracts/fixtures/deduplication. Do not use coverage or implementation branches to select cases.
Task: propose a compact set of pytest tests with stronger oracles for existing behavior, not new functionality. Consider nested JSON metadata across create/read/storage, PATCH preserving omitted fields, filter membership after a committed PATCH, classification leaving a preexisting record unchanged, title boundaries 0/1/2/199/200/201 and invalid create/PATCH inputs. Existing filter tests already exercise enum combinations, query errors and ordering; do not repeat them merely for counts. Expected behavior: valid title length 1..200; invalid requests 422 with body field location and no write; metadata round-trips; omitted PATCH fields remain; missing IDs 404 preserve unrelated items; classification has no persistence effect. Explicit null in PATCH is unresolved: defer that case.
Before code, give case ID -> contract/partition/boundary -> expected response and stored state -> distinct gain or reason to reject. Then return proposed complete test source as text, with the smallest supporting fixture if required. Reuse the in-memory client setup; do not combine client and db_session fixtures. A fresh SQLAlchemy session can check committed state but is not evidence of another physical connection or process. Assert content and errors, not only HTTP status. Limit the proposal to justified additions; no desired test count, no production changes. One subsequent refinement at most. Do not execute checks; the integrator will record real results. State model/configuration only if observable.
```

### B — retained original request

```text
Use $api-integration-structural in this same existing checkout, as the sequential B experiment. Remain read-only: no edits, tests/imports, installs, services, other agents, credentials, commits or publication. The integrating conversation is the only writer.
Confirm whether this skill is in the available catalog and read its actual SKILL.md. Report discovery versus explicit loading separately. Use the ORIGINAL measured baseline, not coverage expanded by experiment A: Coverage.py 7.17.0, --branch --source=app, 148 baseline tests, 248/258 executable statements and 36/38 branch destinations. Missing app/db/database.py lines 18,23,44,46,51,52,53,55; missing branches [17,18] and [20,23]. app/main.py lifespan lines 14,15 are also missing. Read these relevant code files, docs/testing.md and README setup contract. Do not read another implementation or propose production changes.
Expected behavior before code: file-backed SQLite setup creates the requested parent directory; memory/non-SQLite URLs do not create directories; application startup creates its schema; request sessions close on success and consumer error. Use exclusively synthetic data and temporary test resources. No use of the application's default engine/database for persistence; justify how isolation is established before TestClient lifespan runs. No installed database drivers or server dependencies. Prefer useful unit checks on isolated helper decisions and real integration checks where a resource boundary is required. Avoid duplicate business/filter matrices already present.
Return gap -> documented contract -> expected observable result -> proposed test and why its oracle is meaningful. Then provide complete source proposals, with levels/markers and any minimal fixtures. Cover resource cleanup on errors with an observable assertion, not coverage alone. No desired coverage percentage or test count. Explicitly defer unsupported contracts. Do not execute; the integrator will preserve output, review and run the tests. At most one refinement will follow. This session retains A's context; do not claim independent or blinded comparison.
```

## Revised skill evaluation requests

The following are **sanitized excerpts** of the new 2026-10-26 requests: absolute checkout/evidence paths and routing wrappers are omitted. Exact prompts and version/hash/read evidence were retained outside the public tree. They are not replacements for A/B. All five skills were named explicitly; native discovery and another client's support were not demonstrated by these reads.

### Functional — explicit use

```text
Use $api-integration-functional and read its actual SKILL.md.
Report version/hash and catalog availability separately from explicit loading.
Assess create -> partial update -> list/filter from contracts and existing tests.
Map partitions, expected response and stored effects before proposing code.
Reject duplicates; a justified no-addition result is valid. Do not select by
coverage or invent PATCH-null policy. Return proposals as text only; the
integrator alone writes and executes authorized checks.
```

The review identified explicit empty replacement as distinct from omission. One new integration case was accepted after oracle review. A single instruction refinement (2.0.0 ->2.0.1) clarified that execution prerequisites are not required for design-only work; the revised file was explicitly reread, not proven reloaded through a catalog.

### Structural — explicit use

```text
Use $api-integration-structural and read its actual SKILL.md.
Inspect the newly measured parent coverage, source revision, contracts and
existing assertions. Propose a case only for a meaningful uncovered executable
gap; separate risk/oracle suggestions. Keep the denominator fixed.
Do not edit or execute during this read-only selection task.
```

No coverage-selected addition was justified. The reviewer requested provenance absent from Coverage.py JSON; a companion linked the preserved command, 191 case IDs, report hash and unchanged source revision. This was an input-evidence correction without remeasurement, not a fabricated coverage gap.

### Oracle review — explicit use

```text
Use $test-oracle-review and read its actual SKILL.md.
Review the selected metadata/PATCH case, success/error session cleanup, and
two HTTP lifecycle cases against contracts and their helper assertions.
Identify only concrete blocks/improvements/style with scenario and consequence.
Trace the first decisive assertion and checks not reached after a failure.
No execution or edits during this review; do not invent desired product policy.
```

Accepted findings strengthened JSON typing in GET/PATCH and validated complete creation fields/defaults before system baselines. These static oracle gaps were not demonstrated defects in production; overlap across real boundaries was retained.

### Bounded mutation — explicit use

```text
Use $bounded-mutation-evaluation and read its actual SKILL.md.
Reproduce only the known get_db no-close operator in an owned disposable copy.
Run the two focal lifecycle cases without mutation first, then the identical
selection against the one-location mutant, with 60s per subprocess.
Never edit the delivery checkout. Classify assertion failures, survivors,
invalid/setup/timeout results separately and verify cleanup.
```

The valid control passed; both mutated cases failed at close-call verification. A prior operator precondition stopped before mutation because of LF/CRLF matching. Its preserved control/failure was not counted as detection. A later XML-summary parsing correction used existing assertion traces, not another test run.

### HTTP lifecycle — explicit use

```text
Use $http-system-lifecycle and read its actual SKILL.md.
Execute the existing real HTTP journey and normal restart using the project
profile and owned launcher. Use exclusive synthetic SQLite, reserved loopback
port, bounded readiness/requests/stop/lifetime and source/PID checks.
Verify normal exit and owned port/file release. No existing user server,
deployment, crash qualification or global changes.
```

The two strengthened system cases passed; the focal task's three server processes stopped normally. Final regression and preservation checks are reported separately in [the guide](testing.md#current-skill-evaluation--2026-10-26). No causal ranking of prompts/skills or independent human runtime audit is implied.
