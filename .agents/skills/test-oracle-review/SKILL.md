---
name: test-oracle-review
description: Review Python test assertions against requirements and observed evidence; use to detect weak, circular or redundant oracles without generating a new feature.
metadata:
  version: "1.0.0"
---
# Test oracle review
Read the task contract, tests, fixtures and actual results. For every finding identify file/test, scenario, expected property, assertion reached and missing evidence. Distinguish a requirement from behavior observed in code. Never derive both stimulus and expected output from the same production helper.
Review content, errors and data effects, including helper assertions that may fail before later checks. Explain whether overlapping cases cross a useful boundary or repeat the same property. A passing test or coverage percentage is not evidence that every assertion is meaningful.
Return only concrete [blocks], [improves] or [style] findings and keep/revise/combine/discard advice. Do not refactor for cosmetics, change product policy or weaken expectations. Apply/execute only when the current task authorizes it. At most one motivated refinement.

Record requirement/oracle status -> case/operator -> executed result, skill version/hash, rework, human intervention and limitations in the existing testing guide/private evidence. See [method attribution](../../../docs/testing.md#method-origins).
