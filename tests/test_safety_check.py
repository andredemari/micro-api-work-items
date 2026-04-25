import subprocess
import sys
from pathlib import Path

from scripts.install_git_hooks import default_python_command, install_hooks
from scripts.safety_check import Finding, load_policy, run_checks


def run_git(repo_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_path), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def init_repo(tmp_path: Path) -> Path:
    run_git(tmp_path, "init")
    run_git(tmp_path, "config", "user.email", "student@example.com")
    run_git(tmp_path, "config", "user.name", "Student")
    return tmp_path


def write_file(repo_path: Path, relative_path: str, content: str = "content\n") -> None:
    file_path = repo_path / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def failure_ids(findings: list[Finding]) -> set[str]:
    return {finding.detector_id for finding in findings if finding.severity == "fail"}


def warning_ids(findings: list[Finding]) -> set[str]:
    return {finding.detector_id for finding in findings if finding.severity == "warn"}


def test_tracked_sensitive_path_fails_in_temp_repo(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, ".private/note.txt")
    run_git(repo_path, "add", ".private/note.txt")

    findings = run_checks(repo_path, "release", load_policy())

    assert "PATH-PRIVATE-DOTDIR" in failure_ids(findings)


def test_staged_sensitive_path_fails_without_touching_project_repo(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "private/note.txt")
    run_git(repo_path, "add", "private/note.txt")

    findings = run_checks(repo_path, "staged", load_policy())

    assert "PATH-PRIVATE-DIR" in failure_ids(findings)


def test_untracked_private_path_warns_but_does_not_fail(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, ".private/local-note.txt")

    findings = run_checks(repo_path, "working-tree", load_policy())

    assert "PATH-PRIVATE-DOTDIR" in warning_ids(findings)
    assert not failure_ids(findings)


def test_release_mode_fails_on_untracked_private_path(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, ".private/local-note.txt")

    findings = run_checks(repo_path, "release", load_policy())

    assert "PATH-PRIVATE-DOTDIR" in failure_ids(findings)


def test_known_incident_path_in_history_fails_in_temp_repo(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "docs/demo.md", "private content\n")
    run_git(repo_path, "add", "docs/demo.md")
    run_git(repo_path, "commit", "-m", "docs: add private local notes")

    findings = run_checks(repo_path, "history", load_policy())

    assert "HISTORY-KNOWN-INCIDENT" in failure_ids(findings)


def test_tracked_local_artifact_fails(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "local.db")
    run_git(repo_path, "add", "local.db")

    findings = run_checks(repo_path, "release", load_policy())

    assert "ARTIFACT-DATABASE-DB" in failure_ids(findings)


def test_forbidden_public_reference_fails_outside_allowlist(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "README.md", "This file mentions a technical demo.\n")
    run_git(repo_path, "add", "README.md")

    findings = run_checks(repo_path, "release", load_policy())

    assert "PUBLIC-TECHNICAL-DEMO" in failure_ids(findings)


def test_allowed_governance_reference_does_not_fail(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(
        repo_path,
        "docs/security_checks.md",
        "The policy may refer to docs/demo.md as a known incident path.\n",
    )
    run_git(repo_path, "add", "docs/security_checks.md")

    findings = run_checks(repo_path, "release", load_policy())

    assert not failure_ids(findings)


def test_secret_assignment_output_is_redacted(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    raw_value = "alpha-" + "bravo-" + "omega"
    field_name = "pass" + "word"
    write_file(repo_path, "settings.py", f'{field_name} = "{raw_value}"\n')
    run_git(repo_path, "add", "settings.py")

    findings = run_checks(repo_path, "release", load_policy())
    output = "\n".join(finding.format() for finding in findings)

    assert "SECRET-ASSIGNMENT" in failure_ids(findings)
    assert raw_value not in output
    assert raw_value[:5] not in output
    assert raw_value[-5:] not in output
    assert "<redacted>" in output


def test_placeholder_secret_assignment_does_not_fail(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "settings.py", 'token = "<token>"\n')
    run_git(repo_path, "add", "settings.py")

    findings = run_checks(repo_path, "release", load_policy())

    assert "SECRET-ASSIGNMENT" not in failure_ids(findings)


def test_runtime_provider_indicator_fails_in_app_scope(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "app/future_provider.py", "import openai\n")
    run_git(repo_path, "add", "app/future_provider.py")

    findings = run_checks(repo_path, "release", load_policy())

    assert "PROVIDER-OPENAI" in failure_ids(findings)


def test_future_only_provider_docs_do_not_fail(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(
        repo_path,
        "docs/external_provider_plan.md",
        "OpenAI can be discussed here as future-only planning.\n",
    )
    run_git(repo_path, "add", "docs/external_provider_plan.md")

    findings = run_checks(repo_path, "release", load_policy())

    assert not failure_ids(findings)


def test_raw_sql_indicator_is_warning_only(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    write_file(repo_path, "app/query.py", 'db.execute("SELECT 1")\n')
    run_git(repo_path, "add", "app/query.py")

    findings = run_checks(repo_path, "release", load_policy())

    assert "SQL-DB-EXECUTE" in warning_ids(findings)
    assert not failure_ids(findings)


def test_default_hook_python_command_uses_current_interpreter() -> None:
    assert sys.executable in default_python_command()
    assert default_python_command() != "python"


def test_install_hooks_use_selected_python_command(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)

    result = install_hooks(repo_path, python_command="py -3")

    assert result == 0
    assert (repo_path / ".git" / "hooks" / "pre-commit").read_text(encoding="utf-8") == (
        "#!/bin/sh\n"
        'cd "$(git rev-parse --show-toplevel)" || exit 1\n'
        "py -3 scripts/safety_check.py --mode staged\n"
    )
    assert (repo_path / ".git" / "hooks" / "pre-push").read_text(encoding="utf-8") == (
        "#!/bin/sh\n"
        'cd "$(git rev-parse --show-toplevel)" || exit 1\n'
        "py -3 scripts/safety_check.py --mode release\n"
    )


def test_install_hooks_refuse_to_overwrite_existing_hooks(tmp_path: Path) -> None:
    repo_path = init_repo(tmp_path)
    hook_path = repo_path / ".git" / "hooks" / "pre-commit"
    hook_path.write_text("#!/bin/sh\ncustom\n", encoding="utf-8")

    result = install_hooks(repo_path, python_command="py -3")

    assert result == 1
    assert hook_path.read_text(encoding="utf-8") == "#!/bin/sh\ncustom\n"
