---
name: test-oracle-review
description: Review Python test assertions against requirements and execution evidence. Use to find circular expectations, missing effects or unjustified duplication; not to invent product rules or refactor for style.
license: Apache-2.0
metadata:
  version: "2.0.0"
---
# Review test oracles

## When to use
Review whether selected tests can distinguish required behavior from plausible wrong behavior. Static review is useful even when execution is not authorized.

## Inputs and prerequisites
Read the requested requirement/source, selected tests and their helpers/fixtures, execution evidence if available, project profile and review limits. Source reading is sufficient for a static review; report that limitation. No linter or external model service is required.

## Workflow
1. Identify each test's actual stimulus, boundary and expected property. Mark defined contracts, implementation observations and pending policy separately.
2. Trace helper assertions in execution order. Identify the first decisive assertion and which later checks would not be reached if it failed.
3. Check status plus content/types, error location and relevant state effects. Compare the expected value's source with production: calling the same helper for actual and expected creates a circular oracle.
4. Assess overlap by property and boundary. Repetition across a useful integration boundary may be justified; counts alone do not establish redundancy.
5. Return concrete findings before edits. Apply or execute only if the current task permits; recheck only affected behavior after an accepted correction.

## Outputs and verification
For each finding state file/test, scenario, requirement, assertion reached, consequence and classification [blocks], [improves] or [style]. Also report inspected boundaries, absence of findings when warranted and limits. Record version/hash/read/use; never imply independent runtime validation from a static pass.

## Guardrails and stop conditions
Do not invent a defect to justify review. An undefined product rule needs a decision, not an assertion that freezes current behavior. Do not weaken tests, change production, demand cosmetic refactoring or claim security certification. Preserve initial evidence and the task's refinement bound.

## Example
Python equality permits `True == 1`. If a supplied JSON contract distinguishes booleans and numbers, compare a canonical JSON encoding or assert schema-relevant types:
```python
assert response.status_code == 200
body = response.json()
assert type(body["enabled"]) is bool
assert body["enabled"] is True
```
Do not demand such an assertion where the contract allows either type. For a no-write requirement, compare a positive preexisting snapshot with the post-error state; an empty-vs-empty check alone can miss accidental clearing.

Original Python review workflow. It uses contract/structure distinctions from the attributed testing methods and the inspect-before-action pattern, not an OpenSpec workflow. No external reference is required to perform this skill.
