import sys

import pytest

from scripts.install_git_hooks import default_python_command

pytestmark = [pytest.mark.unit, pytest.mark.tooling]


def test_default_hook_python_command_uses_current_interpreter() -> None:
    assert sys.executable in default_python_command()
    assert default_python_command() != "python"
