---
name: api-integration-structural
description: Select meaningful Python test improvements from measured statement and branch gaps while using contracts as the oracle. Use for an actual scoped coverage report, not a percentage target.
license: Apache-2.0
metadata:
  version: "2.0.0"
---
# Evidence-led structural tests

## When to use
Use measured coverage to investigate unexercised behavior. This differs from contract-led selection and from reviewing assertion quality.

## Inputs and prerequisites
Require current source/revision, actual coverage data and command, measured source scope, contracts, existing cases/fixtures and the project test profile. Measurement needs installed Coverage.py/Pytest plus authorized execution; inspecting an existing report requires only file access. Identify uninstrumented subprocesses.

## Workflow
1. Check that the report belongs to the supplied revision and selected cases. Record executable statements, branch destinations and exclusions; do not infer them from a test count.
2. Inspect meaningful missing lines/destinations and link each to a contract-derived expected consequence. A line being executed does not prove that consequence was asserted.
3. Prefer isolated unit checks for local decisions and integration checks for resource boundaries. Do not refactor production merely to create a seam.
4. Compare candidates against the existing suite. If no justified gap exists, report that result; any separate risk/oracle proposal must be labeled as such, not coverage-driven.
5. When authorized, preserve the baseline and candidate sets and remeasure the same production denominator with comparable commands. Record failures and bounded corrections without a default 100% loop.

## Outputs and verification
Return measured gap -> source contract -> expected observable property -> existing/proposed test -> measured result or reason for no addition. Record version/hash/read/use, actual commands, denominators and limitations. Distinguish selection by structure from the oracle's contractual basis.

## Guardrails and stop conditions
Missing/stale coverage blocks claims about gaps, not unrelated authorized analysis. Do not invent missing branches, remove tests, weaken assertions, install tools or change production to improve a percentage. Execution, evidence writes and publication require task authorization. Parent-process coverage does not include HTTP children unless they are instrumented.

## Example
For a project with source package `app`, an authorized comparable measurement might be:
```text
python -B -m coverage run --branch --source=app -m pytest tests/unit tests/integration -q -p no:cacheprovider --basetemp <new-exclusive-directory>
python -B -m coverage json -o <authorized-report-path>
```
Set the coverage data destination outside the public tree using the selected shell. Do not copy placeholder paths literally.

A report with missing cleanup logic can justify a success/error resource-release case if the contract requires cleanup. A report with all measured statements/destinations executed instead yields: "No uncovered executable gap in this scope; assertion strength, child processes and other environments remain separate questions."

Method adapted from open-box-test-generation, aurimrv/go-face-recognition, revision 6c4b8a558a72e4b69edf56394854aefc17769c27 (MIT, copyright 2024 André Oliveira Silva). Original Python instructions; no Go tooling or automatic coverage target. Upstream access is optional, not an execution prerequisite.
