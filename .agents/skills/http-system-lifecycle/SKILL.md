---
name: http-system-lifecycle
description: Exercise an owned Python HTTP process with isolated storage, readiness, normal restart and cleanup. Use for real loopback system checks, not an existing user server or crash qualification.
license: Apache-2.0
metadata:
  version: "2.0.0"
---
# Own the HTTP test lifecycle

## When to use
Validate the process/HTTP/storage boundary and normal restart when in-process clients cannot demonstrate that boundary.

## Inputs and prerequisites
Obtain the application snapshot/entry point, existing launcher/test support, interpreter/dependencies, explicit health response, synthetic storage path, readiness/request/stop/lifetime limits and evidence destination. Needed capabilities: launch and retain a child handle, reserve loopback, request HTTP and verify resource release. Read the project profile; do not assume another client's shell or tools.

## Workflow
1. Establish configuration before application imports. Use exclusive temporary storage and a controlled environment; inspect the launcher before running it.
2. Protect acquisition as well as release of sockets, logs and process handles. Bind and retain an owned loopback port, preferably assigned by the OS; do not race by probing a port then releasing it before launch.
3. Bound readiness polling by deadline and verify health plus endpoint identity, PID/source origins and database path. Process existence or a fixed sleep is not readiness proof.
4. Execute the authorized journey with request timeouts; preserve each response before later operations can fail. Assert typed content, errors and relevant stored state.
5. For normal restart, confirm the old process ended before starting another on the same synthetic database. Compare complete committed records, not only response status.
6. Finalize in `finally`: request normal stop, wait within limits and retain the handle if exit is uncertain. Use only authorized fallback termination on that exact handle. Record forced exit as failure of normal shutdown. Verify owned port/file release and preserve partial evidence.

## Outputs and verification
Return interpreter/source, owned process/endpoint/storage, readiness and operation results, stop reason/exit, release checks and limitations. Record version/hash/read/use. A failed acquisition or uncertain cleanup is a result to investigate, not a successful lifecycle.

## Guardrails and stop conditions
Never connect to the user's running application/database, bind externally, select processes by name, install services or change firewall/global settings. Stop if ownership, isolation, authorization or remaining cleanup time is uncertain. Normal restart does not prove crash recovery, power-loss durability, multiple identities or offline inference.

## Example
For a project-provided `http_process` fixture whose launcher enforces the supplied limits:
```python
server = http_process.start()
try:
    response = server.client.post("/work-items", json={"title": "Synthetic note"})
    assert response.status_code == 201
    created = response.json()
    server.stop()
    assert server.stops[-1]["normal"] is True
    server.start()
    response = server.client.get(f"/work-items/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created
finally:
    server.stop()
```
This fixture is an input capability, not bundled production code or a universal API contract. The task supplies concrete deadlines and health semantics.

Original Python lifecycle workflow. Inspect/propose/execute/closeout boundaries were informed by the preserved MIT testing/OpenSpec references; their CLI, governance and dependencies are not adopted. Upstream access is optional.
