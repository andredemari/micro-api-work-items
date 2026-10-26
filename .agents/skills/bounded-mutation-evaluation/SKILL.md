---
name: bounded-mutation-evaluation
description: Evaluate a supplied small set of deliberate Python faults using pristine controls and isolated copies; use for bounded reproductions and survivor triage, not automatic mutant generation.
metadata:
  version: "1.0.0"
---
# Bounded mutation evaluation
Obtain the exact operators, selected old/new tests, source snapshot, interpreter, resource limits and evidence destination. Require correct controls to pass before applying any operator. Use a fresh isolated copy per mutant and prove only the supplied production location changed; never edit the delivery checkout.
Run one mutation at a time, preserving commands, actual imports, exits and assertion traces. A timeout, syntax/import/setup error or inconclusive resource cleanup is not automatically a detected mutant. Record survivors and assertion locations, including whether later assertions were reached. Do not add tests or change expectations to force detection unless separately authorized.
Close only owned processes/resources and verify source preservation. Known operators are reproductions, not new discoveries. Do not install mutation engines, pursue all survivors or infer a general mutation score from a hand-picked set. At most one problem-motivated instruction refinement.

Record requirement/oracle status -> case/operator -> executed result, skill version/hash, rework, human intervention and limitations in the existing testing guide/private evidence. See [method attribution](../../../docs/testing.md#method-origins).
