---
name: http-system-lifecycle
description: Exercise a Python application as an owned separate HTTP process with synthetic SQLite, readiness, normal restart and cleanup; use for loopback system tests, not deployment or crash qualification.
metadata:
  version: "1.0.1"
---
# Owned HTTP system lifecycle
Use the current task limits and tests/http_process_support.py. Establish a production snapshot, explicit interpreter, temporary database path and controlled environment before importing the app. Reserve an owned loopback socket on port0; verify actual endpoint, PID and source origins. Never connect to an existing user server/database.
Wait for explicit health/identity readiness within15s. Bound requests to5s, graceful stop to10s and each server to90s. No reload, multiple workers, external binds or arbitrary sleeps used as readiness proof. Always finalize in finally; forced termination is a failure of normal shutdown, not a successful persistence test.
For normal restart, first confirm the old process ended, then reuse only the same synthetic database with a new process/port and compare committed content. Preserve logs, identifiers and partial results. Check port and file release; stop only owned resources. Never present normal restart as crash/power-loss durability or two clients as authenticated users. Do not install services or alter global/network/security settings. At most one motivated refinement.

Record requirement/oracle status -> case/operator -> executed result, skill version/hash, rework, human intervention and limitations in the existing testing guide/private evidence. See [method attribution](../../../docs/testing.md#method-origins).

Protect acquisition of logs/process handles as well as their release. Never discard a live handle when shutdown is unconfirmed; preserve partial HTTP results before later operations can fail.
