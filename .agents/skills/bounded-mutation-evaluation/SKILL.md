---
name: bounded-mutation-evaluation
description: Evaluate supplied deliberate Python faults with pristine controls and isolated copies. Use for bounded reproductions and survivor analysis, not automatic campaigns or new bug claims.
license: Apache-2.0
metadata:
  version: "2.0.0"
---
# Evaluate a bounded mutation

## When to use
Check whether selected assertions detect an explicitly supplied wrong behavior, or reproduce a known result to validate the procedure.

## Inputs and prerequisites
Require the exact source snapshot/revision, operator and single target, selected tests, interpreter/dependencies, timeout/resource limits and authorized evidence destination. Needed capabilities: create private isolated copies, edit only those copies, run bounded subprocesses and verify their cleanup. No mutation-engine installation is required for a supplied operator.

## Workflow
1. Snapshot/hash the delivery checkout and prepare a pristine isolated control. Confirm import/source origins and synthetic database isolation; run the selected tests without mutation first.
2. If the control fails, classify and resolve its cause within scope before interpreting a mutant. Preserve failed controls instead of counting them as detections.
3. Create a separate copy per operator. Apply exactly the supplied change and compare hashes/diff: no delivery-source, test or expectation changes.
4. Run the same selected cases with the same limits. Record assertion traces and the first decisive failure. Classify detected assertion, survivor, invalid mutant, configuration/import/setup failure, timeout or uncertain result separately.
5. Close only owned resources, verify the original checkout is unchanged and preserve the variant/evidence. Stop at the supplied operator/refinement limit.

## Outputs and verification
Return control -> operator/target -> cases -> exit and decisive assertion -> classification, including survivors and checks not reached. Record version/hash/read/use and cleanup. A reproduction remains a reproduction; a hand-picked set does not produce a general mutation score.

## Guardrails and stop conditions
Never apply a mutant to the delivery checkout. Do not add tests or adjust expectations to force detection unless separately authorized. Uncertain origins, failing controls or unconfirmed cleanup block the affected interpretation. No implicit installs, wider campaigns or live data.

## Example
For a supplied session-close contract, a bounded operator may replace only the copied dependency's `db.close()` with `pass`. A focal test may observe:
```python
close_spy.assert_called_once_with()
assert pool.checkedout() == 0
```
If the first assertion sees zero calls, report that assertion as the detector; the following pool check was not reached. Passing controls plus this failure demonstrate sensitivity to this operator, not a bug in the original application.

Method adapted from mutation-test-generation, aurimrv/go-face-recognition-unico, revision 6c4b8a558a72e4b69edf56394854aefc17769c27 (MIT, copyright 2024 André Oliveira Silva). Original Python instructions; no gomutants installation or open-ended survivor elimination.
