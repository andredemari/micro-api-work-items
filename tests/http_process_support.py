"""Owned loopback test process; no production or global configuration changes."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import threading
import time

import httpx


def _write(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temporary.replace(path)


def _hashes(source):
    return {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted((source / "app").rglob("*.py"))}


def _exclusive_read(path):
    if not path.exists():
        return True
    if os.name != "nt":
        with path.open("rb"):
            return True  # Process exit is observed; this is not a Windows sharing probe.
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                  ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.CreateFileW(str(path), 0x80000000, 0, None, 3, 0x80, None)
    if handle in (None, ctypes.c_void_p(-1).value):
        return False
    return bool(kernel.CloseHandle(handle))


class HttpProcess:
    def __init__(self, workspace, record):
        self.workspace = Path(workspace).resolve()
        self.workspace.mkdir(parents=True)
        self.source = self.workspace / "source"
        app_source = Path(__file__).resolve().parent.parent / "app"
        shutil.copytree(app_source, self.source / "app", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.source_hashes = _hashes(self.source)
        self.database = self.workspace / "synthetic.sqlite3"
        self.record = record
        self.process = None
        self.client = None
        self.stops = []
        self.starts = []

    def start(self):
        if self.process is not None:
            raise RuntimeError("Stop the owned process before starting another")
        window = os.environ.get("HTTP_TEST_WINDOW_FILE")
        if window:
            times = json.loads(Path(window).read_text(encoding="utf-8"))
            remaining = (datetime.fromisoformat(times["cleanup_start_utc"]) - datetime.now(timezone.utc)).total_seconds()
            if remaining < 100:
                raise RuntimeError("Insufficient approved test window; preserve and clean up")
        self.number = len(self.starts) + 1
        self.endpoint = self.workspace / f"endpoint-{self.number}.json"
        self.lifecycle = self.workspace / f"lifecycle-{self.number}.json"
        self.out = None
        self.err = None
        env = {key: value for key, value in os.environ.items()
               if key.upper() in {"SYSTEMROOT", "WINDIR", "PATH", "PATHEXT", "COMSPEC", "LANG"}}
        env.update(TEMP=str(self.workspace), TMP=str(self.workspace), TMPDIR=str(self.workspace))
        command = [sys.executable, "-I", "-B", "-X", "utf8", "-u", str(Path(__file__).resolve()),
                   "--serve", str(self.source), str(self.database), str(self.endpoint), str(self.lifecycle)]
        try:
            self.out = (self.workspace / f"server-{self.number}.stdout.txt").open("wb")
            self.err = (self.workspace / f"server-{self.number}.stderr.txt").open("wb")
            self.process = subprocess.Popen(command, cwd=self.workspace, env=env, stdin=subprocess.PIPE,
                                            stdout=self.out, stderr=self.err, text=True, encoding="utf-8")
        except BaseException as error:
            for handle in (self.out, self.err):
                if handle is not None:
                    handle.close()
            self.record("HTTP-PROCESS-START-FAILED", {"error_type": type(error).__name__, "error": str(error)})
            raise
        deadline = time.monotonic() + 15
        try:
            while time.monotonic() < deadline:
                if self.process.poll() is not None:
                    raise RuntimeError(f"Server exited during readiness; inspect {self.err.name}")
                if self.endpoint.exists():
                    data = json.loads(self.endpoint.read_text(encoding="utf-8"))
                    assert data["host"] == "127.0.0.1" and data["pid"] == self.process.pid
                    assert data["database"] == str(self.database)
                    assert data["source_hashes"] == self.source_hashes
                    assert all(Path(p).resolve().is_relative_to(self.source) for p in data["origins"].values())
                    self.url = f"http://127.0.0.1:{data['port']}"
                    self.port = data["port"]
                    self.client = httpx.Client(base_url=self.url, timeout=5, trust_env=False)
                    response = self.client.get("/health", timeout=1)
                    assert response.status_code == 200
                    assert response.json() == {"status": "ok", "service": "micro-api-work-items"}
                    self.starts.append(data)
                    self.record("HTTP-PROCESS-START", {**data, "command": command})
                    return self
                threading.Event().wait(0.02)  # Bounded readiness polling, not a fixed startup sleep.
            raise TimeoutError("Readiness exceeded 15 seconds")
        except BaseException:
            self.stop(require_normal=False)
            raise

    def new_client(self):
        return httpx.Client(base_url=self.url, timeout=5, trust_env=False)

    def stop(self, require_normal=True):
        if self.process is None:
            return
        process = self.process
        normal = False
        forced = False
        if self.client is not None:
            self.client.close()
            self.client = None
        try:
            if process.poll() is None:
                try:
                    process.stdin.write("stop\n")
                    process.stdin.flush()
                except (BrokenPipeError, OSError):
                    pass
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                forced = True
                process.terminate()  # Only the exact owned Popen handle.
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()  # Same owned handle; never a process selected by name/port.
                    process.wait(timeout=5)
            life = json.loads(self.lifecycle.read_text(encoding="utf-8")) if self.lifecycle.exists() else {}
            normal = process.returncode == 0 and life.get("shutdown_reason") == "stdin-stop" and not forced
            port_released = not hasattr(self, "port")
            deadline = time.monotonic() + 3
            while hasattr(self, "port") and time.monotonic() < deadline:
                try:
                    with socket.socket() as probe:
                        probe.bind(("127.0.0.1", self.port))
                    port_released = True
                    break
                except OSError:
                    threading.Event().wait(0.05)
            data = {"pid": process.pid, "exit_code": process.returncode, "normal": normal,
                    "forced": forced, "port_released": port_released,
                    "database_released": _exclusive_read(self.database), "lifecycle": life,
                    "source_unchanged": _hashes(self.source) == self.source_hashes}
            self.stops.append(data)
            self.record("HTTP-PROCESS-STOP", data)
            if require_normal and not all((normal, port_released, data["database_released"], data["source_unchanged"])):
                raise RuntimeError(f"Owned HTTP process cleanup not qualified: {data}")
        except BaseException as error:
            self.record("HTTP-PROCESS-CLEANUP-FAILED", {"pid": process.pid,
                "confirmed_exited": process.poll() is not None,
                "error_type": type(error).__name__, "error": str(error)})
            raise
        finally:
            # Retain management/log handles if termination could not be confirmed.
            if process.poll() is not None:
                process.stdin.close()
                self.out.close()
                self.err.close()
                self.process = None


def _serve(source, database, endpoint, lifecycle):
    source, database, endpoint, lifecycle = map(lambda p: Path(p).resolve(), (source, database, endpoint, lifecycle))
    workspace = source.parent
    assert database.parent == workspace and database.name == "synthetic.sqlite3"
    assert endpoint.parent == workspace and lifecycle.parent == workspace
    assert not any(name == "app" or name.startswith("app.") for name in sys.modules)
    from sqlalchemy.engine import URL
    os.environ["DATABASE_URL"] = str(URL.create("sqlite", database=str(database)))
    sys.path.insert(0, str(source))
    import uvicorn
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    listener.setblocking(False)
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config("app.main:app", host="127.0.0.1", port=port,
        loop="asyncio", http="h11", ws="none", lifespan="on", access_log=False,
        log_level="warning", timeout_graceful_shutdown=5, workers=1))
    done = threading.Event()
    reason = []

    def stop(why):
        if not reason:
            reason.append(why)
        server.should_exit = True

    def control():
        line = sys.stdin.readline()
        stop("stdin-stop" if line.strip() == "stop" else "stdin-eof")

    def ready():
        while not server.started and not done.wait(0.02):
            pass
        if server.started and not done.is_set():
            _write(endpoint, {"pid": os.getpid(), "host": "127.0.0.1", "port": port,
                "database": str(database), "source_hashes": _hashes(source),
                "origins": {name: sys.modules[name].__file__ for name in ("app.main", "app.db.database")}})

    threading.Thread(target=control, daemon=True).start()
    threading.Thread(target=ready, daemon=True).start()
    timer = threading.Timer(90, lambda: stop("watchdog-90s"))
    timer.daemon = True
    timer.start()
    try:
        server.run(sockets=[listener])
    finally:
        done.set()
        timer.cancel()
        listener.close()
        _write(lifecycle, {"pid": os.getpid(), "shutdown_reason": reason[0] if reason else "server-exit",
                           "listener_closed": listener.fileno() == -1})


if __name__ == "__main__":
    if len(sys.argv) != 6 or sys.argv[1] != "--serve":
        raise SystemExit("This helper is launched only by the owned HTTP fixture")
    _serve(*sys.argv[2:])
