"""Deterministic repository safety checks for public submission readiness."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_POLICY_PATH = Path(__file__).with_name("safety_policy.json")
VALID_MODES = ("working-tree", "staged", "history", "release")
LOCAL_ONLY_IGNORED_PATHS = {"docs/demo.md"}


@dataclass(frozen=True)
class Finding:
    severity: str
    detector_id: str
    message: str
    path: str | None = None
    line: int | None = None
    redacted: str | None = None

    def format(self) -> str:
        location = self.path or "<repository>"
        if self.line is not None:
            location = f"{location}:{self.line}"

        parts = [
            self.severity.upper(),
            self.detector_id,
            location,
            self.message,
        ]
        if self.redacted:
            parts.append(f"value={self.redacted}")
        return " | ".join(parts)


def load_policy(policy_path: Path = DEFAULT_POLICY_PATH) -> dict:
    return json.loads(policy_path.read_text(encoding="utf-8"))


def normalize_path(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def run_git(repo_path: Path, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_path), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def ensure_git_repo(repo_path: Path) -> Path:
    result = run_git(repo_path, ["rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        raise RuntimeError(f"not a Git repository: {repo_path}")
    return Path(result.stdout.strip())


def split_nul(output: str) -> list[str]:
    return [item for item in output.split("\0") if item]


def git_paths(repo_path: Path, args: Sequence[str]) -> list[str]:
    result = run_git(repo_path, [*args, "-z"])
    if result.returncode != 0:
        return []
    return [normalize_path(path) for path in split_nul(result.stdout)]


def tracked_paths(repo_path: Path) -> list[str]:
    return git_paths(repo_path, ["ls-files"])


def staged_paths(repo_path: Path) -> list[str]:
    return git_paths(repo_path, ["diff", "--cached", "--name-only", "--diff-filter=ACMRT"])


def visible_untracked_paths(repo_path: Path) -> list[str]:
    return git_paths(repo_path, ["ls-files", "--others", "--exclude-standard"])


def ignored_untracked_paths(repo_path: Path) -> list[str]:
    return git_paths(repo_path, ["ls-files", "--others", "--ignored", "--exclude-standard"])


def untracked_paths(repo_path: Path) -> list[str]:
    visible = visible_untracked_paths(repo_path)
    ignored = ignored_untracked_paths(repo_path)
    return sorted(set(visible + ignored))


def untracked_paths_for_sensitive_check(repo_path: Path) -> list[str]:
    ignored_local_only = {
        normalize_path(path)
        for path in ignored_untracked_paths(repo_path)
        if normalize_path(path) in LOCAL_ONLY_IGNORED_PATHS
    }
    return [
        path
        for path in untracked_paths(repo_path)
        if normalize_path(path) not in ignored_local_only
    ]


def match_entry(path: str, entry: dict) -> bool:
    path = normalize_path(path)
    pattern = normalize_path(entry["pattern"])
    kind = entry.get("kind", "glob")

    if kind == "exact":
        return path == pattern
    if kind == "prefix":
        prefix = pattern.rstrip("/")
        return path == prefix or path.startswith(f"{prefix}/")
    if kind == "suffix":
        return path.endswith(pattern)
    if kind == "segment":
        return pattern in path.split("/")
    if kind == "glob":
        return fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(Path(path).name, pattern)
    raise ValueError(f"unknown path policy kind: {kind}")


def matches_any(path: str, entries: Iterable[dict]) -> dict | None:
    for entry in entries:
        if match_entry(path, entry):
            return entry
    return None


def matches_glob(path: str, patterns: Iterable[str]) -> bool:
    normalized = normalize_path(path)
    return any(fnmatch.fnmatchcase(normalized, normalize_path(pattern)) for pattern in patterns)


def read_worktree_text(repo_path: Path, path: str) -> str | None:
    file_path = repo_path / path
    if not file_path.is_file():
        return None
    try:
        return file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def read_staged_text(repo_path: Path, path: str) -> str | None:
    result = run_git(repo_path, ["show", f":{path}"])
    if result.returncode != 0:
        return None
    return result.stdout


def redacted_value(value: str) -> str:
    return "<redacted>"


def is_placeholder(value: str, placeholders: set[str]) -> bool:
    normalized = value.strip().strip("\"'").lower()
    if normalized in placeholders:
        return True
    if normalized.startswith("<") and normalized.endswith(">"):
        return True
    if normalized.startswith("${") and normalized.endswith("}"):
        return True
    if set(normalized) <= {"x", "*"}:
        return True
    return False


def check_path_policy(paths: Iterable[str], entries: list[dict], severity: str, message: str) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(set(paths)):
        entry = matches_any(path, entries)
        if entry:
            findings.append(
                Finding(
                    severity=severity,
                    detector_id=entry["id"],
                    path=path,
                    message=message,
                )
            )
    return findings


def check_public_references(repo_path: Path, paths: Iterable[str], policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    scopes = policy["public_reference_scopes"]
    allowlist = set(policy.get("public_reference_allowlist_paths", []))
    references = policy["forbidden_public_references"]

    for path in sorted(set(paths)):
        if path in allowlist or not matches_glob(path, scopes):
            continue
        text = read_worktree_text(repo_path, path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            lowered = line.lower()
            for reference in references:
                if reference["text"].lower() in lowered:
                    findings.append(
                        Finding(
                            severity="fail",
                            detector_id=reference["id"],
                            path=path,
                            line=line_number,
                            message="forbidden public reference found",
                        )
                    )
    return findings


def check_secret_text(path: str, text: str, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    detectors = [(detector["id"], re.compile(detector["pattern"])) for detector in policy["secret_detectors"]]
    assignment = policy["assignment_secret_detector"]
    assignment_pattern = re.compile(assignment["pattern"])
    placeholders = {value.lower() for value in policy.get("placeholder_values", [])}

    for line_number, line in enumerate(text.splitlines(), start=1):
        for detector_id, pattern in detectors:
            match = pattern.search(line)
            if match:
                findings.append(
                    Finding(
                        severity="fail",
                        detector_id=detector_id,
                        path=path,
                        line=line_number,
                        message="secret-like structured value found",
                    )
                )

        match = assignment_pattern.search(line)
        if match:
            value = match.group(2)
            if not is_placeholder(value, placeholders):
                findings.append(
                    Finding(
                        severity="fail",
                        detector_id=assignment["id"],
                        path=path,
                        line=line_number,
                        message="secret-like assignment found",
                        redacted=redacted_value(value),
                    )
                )

    return findings


def check_secrets_in_worktree(repo_path: Path, paths: Iterable[str], policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(set(paths)):
        text = read_worktree_text(repo_path, path)
        if text is not None:
            findings.extend(check_secret_text(path, text, policy))
    return findings


def check_secrets_in_staged(repo_path: Path, paths: Iterable[str], policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(set(paths)):
        text = read_staged_text(repo_path, path)
        if text is not None:
            findings.extend(check_secret_text(path, text, policy))
    return findings


def check_history(repo_path: Path, policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    for incident in policy["known_incident_paths"]:
        path = incident["path"]
        result = run_git(repo_path, ["log", "--all", "--", path])
        if result.returncode == 0 and result.stdout.strip():
            findings.append(
                Finding(
                    severity="fail",
                    detector_id=incident["id"],
                    path=path,
                    message="known incident path appears in Git history",
                )
            )
    return findings


def check_runtime_provider_guardrails(repo_path: Path, paths: Iterable[str], policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    runtime_scopes = policy["runtime_scopes"]
    provider_terms = [(term["id"], re.compile(term["pattern"])) for term in policy["runtime_provider_terms"]]
    network_patterns = [(item["id"], re.compile(item["pattern"])) for item in policy["provider_network_patterns"]]
    provider_paths = policy["provider_runtime_path_patterns"]

    for path in sorted(set(paths)):
        if matches_any(path, provider_paths):
            findings.append(
                Finding(
                    severity="fail",
                    detector_id=matches_any(path, provider_paths)["id"],
                    path=path,
                    message="future provider runtime file requires explicit approval",
                )
            )

        if not matches_glob(path, runtime_scopes):
            continue

        text = read_worktree_text(repo_path, path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for detector_id, pattern in provider_terms:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            severity="fail",
                            detector_id=detector_id,
                            path=path,
                            line=line_number,
                            message="runtime external provider indicator found",
                        )
                    )

            if path.startswith("app/providers/"):
                for detector_id, pattern in network_patterns:
                    if pattern.search(line):
                        findings.append(
                            Finding(
                                severity="fail",
                                detector_id=detector_id,
                                path=path,
                                line=line_number,
                                message="network call indicator found in provider runtime scope",
                            )
                        )
    return findings


def check_sql_warnings(repo_path: Path, paths: Iterable[str], policy: dict) -> list[Finding]:
    findings: list[Finding] = []
    patterns = [(item["id"], re.compile(item["pattern"])) for item in policy["sql_warning_patterns"]]

    for path in sorted(set(paths)):
        if not path.startswith("app/") or not path.endswith(".py"):
            continue
        text = read_worktree_text(repo_path, path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            for detector_id, pattern in patterns:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            severity="warn",
                            detector_id=detector_id,
                            path=path,
                            line=line_number,
                            message="raw SQL indicator found; review manually",
                        )
                    )
    return findings


def release_reminders() -> list[Finding]:
    return [
        Finding(
            severity="warn",
            detector_id="RELEASE-REMINDER",
            message="before publication, confirm remote visibility, old commits, and use git archive instead of manual ZIP",
        )
    ]


def run_checks(repo_path: Path, mode: str, policy: dict) -> list[Finding]:
    repo_path = ensure_git_repo(repo_path)
    tracked = tracked_paths(repo_path)
    staged = staged_paths(repo_path)
    findings: list[Finding] = []

    if mode == "working-tree":
        findings.extend(
            check_path_policy(
                untracked_paths_for_sensitive_check(repo_path),
                policy["sensitive_paths"],
                "warn",
                "suspicious private path exists locally; do not stage or track",
            )
        )

    if mode == "release":
        findings.extend(
            check_path_policy(
                untracked_paths_for_sensitive_check(repo_path),
                policy["sensitive_paths"],
                "fail",
                "suspicious private path exists locally; remove it before release packaging",
            )
        )

    if mode in {"working-tree", "staged", "release"}:
        findings.extend(
            check_path_policy(
                staged,
                policy["sensitive_paths"],
                "fail",
                "sensitive/private path is staged",
            )
        )
        findings.extend(check_secrets_in_staged(repo_path, staged, policy))

    if mode in {"working-tree", "release"}:
        findings.extend(
            check_path_policy(
                tracked,
                policy["sensitive_paths"],
                "fail",
                "sensitive/private path is tracked",
            )
        )
        findings.extend(
            check_path_policy(
                tracked,
                policy["tracked_artifact_paths"],
                "fail",
                "local artifact is tracked",
            )
        )
        findings.extend(check_public_references(repo_path, tracked, policy))
        findings.extend(check_secrets_in_worktree(repo_path, tracked, policy))
        findings.extend(check_runtime_provider_guardrails(repo_path, tracked, policy))
        findings.extend(check_sql_warnings(repo_path, tracked, policy))

    if mode in {"history", "release"}:
        findings.extend(check_history(repo_path, policy))

    if mode == "release":
        findings.extend(release_reminders())

    return findings


def print_findings(findings: Iterable[Finding]) -> None:
    for finding in findings:
        print(finding.format())


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic repository safety checks.")
    parser.add_argument("--mode", choices=VALID_MODES, default="release")
    parser.add_argument("--repo", default=".", help="repository path to inspect")
    parser.add_argument("--policy", default=str(DEFAULT_POLICY_PATH), help="safety policy JSON path")
    args = parser.parse_args(argv)

    try:
        policy = load_policy(Path(args.policy))
        findings = run_checks(Path(args.repo), args.mode, policy)
    except RuntimeError as exc:
        print(f"FAIL | SAFETY-CHECK-ERROR | <repository> | {exc}", file=sys.stderr)
        return 2

    print_findings(findings)
    return 1 if any(finding.severity == "fail" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
