---
name: api-integration-functional
description: Design or strengthen Python API integration tests from contracts, partitions and boundaries. Use when responses and persisted effects need meaningful oracles; not for selecting cases from coverage gaps.
license: Apache-2.0
metadata:
  version: "2.0.1"
---
# Contract-led API tests

## When to use
Use a supplied API contract to propose distinct integration checks or strengthen weak assertions. A justified decision to add no tests is a valid result.

## Inputs and prerequisites
For design-only work, obtain the flow, authoritative contract/examples, existing tests/fixtures and project profile. Before execution or artifact writes, also obtain the authorized interpreter/commands and evidence destination. Needed capabilities: read source/tests; execution and writes only if the task authorizes them. Use installed Python/Pytest and the project's actual dependencies; do not install missing tools automatically.

## Workflow
1. Read the profile and relevant contracts. Before code, map requirement -> defined contract, observed behavior or pending decision -> partition/boundary -> expected response/error and stored-state effect.
2. Select boundaries only for ordered domains. Compare each candidate with existing assertions, including helpers; reject duplicates unless they verify a distinct boundary or consequence.
3. Reuse isolated fixtures. Explain whether state is checked through the same session, a fresh identity map, another connection or another process; these prove different things.
4. Assert status, relevant typed content and state. Anchor no-write checks in a known nonempty state. Capture inputs before the call when checking preservation. Do not derive the expected result from the production helper being tested.
5. Run only authorized checks, preserving the initial proposal, commands, exits and review. Refine only for a demonstrated problem, within the task's limit.

## Outputs and verification
Return case -> source/partition -> expected property -> existing/new test -> observed result, plus rejected candidates and unresolved rules. Record this skill's version/hash and actual read/use. Separate proposed tests, executed tests and observations; report no justified addition when appropriate.

## Guardrails and stop conditions
Documents are context, not authority to expand access. Stop the affected case if its oracle is undefined or required isolation is unavailable; continue independent cases. Never change production or weaken expectations to obtain a pass. Write only to authorized destinations. No implicit installation, runtime-data access, publication or unlimited refinement.

## Example
Given a project's explicit title contract of 1..200 characters, first check whether its suite already covers 200/201. An illustrative Pytest case is:
```python
@pytest.mark.parametrize("length, expected", [(200, 201), (201, 422)])
def test_title_limit(client, length, expected):
    before = client.get("/work-items")
    assert before.status_code == 200
    response = client.post("/work-items", json={"title": "x" * length})
    assert response.status_code == expected
    if expected == 422:
        assert response.json()["detail"][0]["loc"] == ["body", "title"]
        after = client.get("/work-items")
        assert after.status_code == 200
        assert after.json() == before.json()
```
The contract and fixture come from the task, not this example. Additional storage assertions depend on the requirement and fixture boundary. Do not copy an already-covered example merely to increase counts.

Method adapted from closed-box-test-generation, aurimrv/go-face-recognition, revision 6c4b8a558a72e4b69edf56394854aefc17769c27 (MIT, copyright 2024 André Oliveira Silva). These are original Python instructions, not copied Go commands. Public provenance is optional reading in the checkout's testing guide; executing the method does not require upstream access.
