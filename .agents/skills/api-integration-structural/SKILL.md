---
name: api-integration-structural
description: Improve Python tests using measured line and branch gaps while deriving expected results from contracts; use for a supplied Coverage.py baseline, not a coverage percentage target.
metadata:
  version: "1.0.0"
---
# Evidence-led structural tests

Read applicable repository instructions and `docs/testing.md`. Obtain the production scope, actual baseline coverage, contract, existing tests and authorized environment. If coverage is unavailable, report the dependency instead of inventing gaps or installing tools automatically.

1. Inspect relevant uncovered lines and branch destinations in the supplied baseline. Explain which meaningful behavior is unverified; execution of a line alone is not an assertion.
2. Link each candidate to a measured gap and a contract-derived oracle. Prefer isolated unit tests for pure logic and integration tests for real boundaries. Do not refactor production merely to create a test seam.
3. Preserve a fixed production denominator and separate candidate sets. Measure the baseline and requested combinations under comparable commands; do not use another experiment's expanded coverage as the original baseline.
4. Execute authorized checks, review the assertions and record actual failures and corrections. Do not weaken tests or pursue an assumed 100% target. Stop at the agreed refinement limit; record deferred or ambiguous behaviors.
5. Return gap -> contract -> test -> measured result, including redundancy, remaining gaps and limits. Coverage does not establish semantic correctness, deployment or security. Do not install tools, access runtime data or publish implicitly.

See the attribution and Python adaptation in [the testing guide](../../../docs/testing.md#method-origins).

## Traceability and oracle status

For each relevant case, link source/requirement -> defined contract, observed behavior or pending decision -> partition/boundary/branch -> stable case ID -> actual result and run ID. Keep the matrix in docs/testing.md and raw results at the authorized private destination. Observed outputs are not normative expectations. Record skill version/hash, actual reading/use, ambiguity, rework and human intervention. At most one problem-motivated refinement; do not generate work merely to justify the skill.

If the supplied baseline has no uncovered executable lines/branches, report that fact. Review whether assertions verify consequences; do not invent coverage gaps or claim authorship of risk-selected cases. Child-process HTTP execution is outside parent-only coverage unless explicitly instrumented.
