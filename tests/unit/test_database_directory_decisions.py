from unittest.mock import Mock

import pytest

from app.db import database


pytestmark = [pytest.mark.unit, pytest.mark.structural]


@pytest.mark.parametrize(
    "database_url",
    [
        pytest.param("sqlite://", id="sqlite-without-file"),
        pytest.param("sqlite:///:memory:", id="sqlite-memory"),
        pytest.param(
            "postgresql:///synthetic",
            id="non-sqlite-url-only",
        ),
    ],
)
def test_directory_helper_skips_urls_without_a_sqlite_file(
    monkeypatch: pytest.MonkeyPatch,
    database_url: str,
) -> None:
    # Only parse the URL and exercise the helper's decision.
    # No engine or non-SQLite driver is created.
    mkdir = Mock()

    with monkeypatch.context() as patch:
        patch.setattr(database.Path, "mkdir", mkdir)

        database.ensure_sqlite_parent_directory(database_url)

        mkdir.assert_not_called()
