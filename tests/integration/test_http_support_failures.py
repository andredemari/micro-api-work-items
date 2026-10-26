import subprocess
from unittest.mock import Mock

import pytest
import http_process_support as support

pytestmark = [pytest.mark.integration, pytest.mark.tooling]


def test_launch_failure_closes_acquired_log_handles(tmp_path, monkeypatch):
    observations = []
    server = support.HttpProcess(tmp_path / "launch", lambda *args: observations.append(args))
    monkeypatch.setattr(support.subprocess, "Popen", Mock(side_effect=OSError("synthetic launch failure")))
    with pytest.raises(OSError, match="synthetic launch failure"):
        server.start()
    assert server.process is None
    assert server.out.closed and server.err.closed
    assert observations[-1][0] == "HTTP-PROCESS-START-FAILED"


def test_unconfirmed_stop_retains_owned_handle_and_failure_record(tmp_path):
    observations = []
    server = support.HttpProcess(tmp_path / "unconfirmed", lambda *args: observations.append(args))
    process = Mock(pid=12345, returncode=None)
    process.poll.return_value = None
    process.wait.side_effect = subprocess.TimeoutExpired("synthetic-owned-process", 1)
    server.process = process
    server.out = (tmp_path / "synthetic.stdout").open("wb")
    server.err = (tmp_path / "synthetic.stderr").open("wb")
    try:
        with pytest.raises(subprocess.TimeoutExpired):
            server.stop()
        assert server.process is process
        assert process.terminate.call_count == 1
        assert process.kill.call_count == 1
        assert not server.out.closed and not server.err.closed
        assert observations[-1][0] == "HTTP-PROCESS-CLEANUP-FAILED"
        assert observations[-1][1]["confirmed_exited"] is False
    finally:
        # The executor is a Mock; no PID is signalled or operating-system process created.
        server.out.close()
        server.err.close()
        server.process = None
