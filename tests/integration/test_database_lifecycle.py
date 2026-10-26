from collections.abc import Iterator
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine, URL
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

import app.main as main_module
from app.db import database
from app.models.work_item_model import WorkItem


pytestmark = [pytest.mark.integration, pytest.mark.structural]


@pytest.fixture()
def synthetic_engine(tmp_path: Path) -> Iterator[Engine]:
    """A separate file-backed SQLite engine for each test."""
    engine = create_engine(
        URL.create(
            "sqlite",
            database=str(tmp_path / "synthetic.sqlite3"),
        ),
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
        pool_size=1,
        max_overflow=0,
        pool_timeout=1,
    )
    try:
        yield engine
    finally:
        engine.dispose()


def test_file_sqlite_setup_creates_parent_and_preserves_existing_files(
    tmp_path: Path,
) -> None:
    database_file = tmp_path / "new" / "nested" / "synthetic.sqlite3"
    database_url = str(
        URL.create("sqlite", database=str(database_file))
    )

    assert not database_file.parent.exists()

    database.ensure_sqlite_parent_directory(database_url)

    assert database_file.parent.is_dir()

    sentinel = database_file.parent / "preserve.txt"
    sentinel.write_text("synthetic sentinel", encoding="utf-8")

    database.ensure_sqlite_parent_directory(database_url)

    assert database_file.parent.is_dir()
    assert sentinel.read_text(encoding="utf-8") == "synthetic sentinel"


@pytest.mark.api
def test_application_lifespan_creates_usable_isolated_schema(
    synthetic_engine: Engine,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    temporary_sessions = sessionmaker(
        bind=synthetic_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    # Establish isolation before entering the real application's lifespan.
    monkeypatch.setattr(database, "engine", synthetic_engine)
    monkeypatch.setattr(database, "SessionLocal", temporary_sessions)
    monkeypatch.setattr(
        main_module.app,
        "dependency_overrides",
        {},
    )

    assert inspect(synthetic_engine).get_table_names() == []

    with TestClient(main_module.app) as client:
        assert WorkItem.__table__.name in (
            inspect(synthetic_engine).get_table_names()
        )

        response = client.post(
            "/work-items",
            json={"title": "Synthetic startup verification"},
        )

        assert response.status_code == 201
        created = response.json()
        assert created["title"] == "Synthetic startup verification"
        assert isinstance(created["id"], int)
        assert created["id"] > 0

        # This session is bound explicitly to the temporary engine.
        with Session(synthetic_engine) as db:
            stored = db.get(WorkItem, created["id"])
            assert stored is not None
            assert stored.title == "Synthetic startup verification"

    assert synthetic_engine.pool.checkedout() == 0


class SyntheticConsumerError(RuntimeError):
    pass


@pytest.mark.parametrize(
    "consumer_fails",
    [
        pytest.param(False, id="success"),
        pytest.param(True, id="consumer-error"),
    ],
)
def test_request_session_closes_and_releases_connection(
    synthetic_engine: Engine,
    monkeypatch: pytest.MonkeyPatch,
    consumer_fails: bool,
) -> None:
    temporary_sessions = sessionmaker(
        bind=synthetic_engine,
        expire_on_commit=False,
    )
    sessions: list[Session] = []
    close_spies: list[Mock] = []
    consumer_checkouts: list[int] = []
    failure = SyntheticConsumerError("synthetic consumer failure")

    def tracked_session_factory() -> Session:
        session = temporary_sessions()
        close_spy = Mock(wraps=session.close)
        monkeypatch.setattr(session, "close", close_spy)
        sessions.append(session)
        close_spies.append(close_spy)
        return session

    monkeypatch.setattr(
        database,
        "SessionLocal",
        tracked_session_factory,
    )

    # A synthetic app exercises FastAPI's real dependency unwinding.
    # It has no production lifespan or default database dependency override.
    probe_app = FastAPI()

    @probe_app.get("/probe")
    def consume_session(
        db: Session = Depends(database.get_db),
    ) -> dict[str, int]:
        value = db.scalar(text("SELECT 1"))
        assert value == 1
        consumer_checkouts.append(
            synthetic_engine.pool.checkedout()
        )
        if consumer_fails:
            raise failure
        return {"value": value}

    try:
        with TestClient(
            probe_app,
            raise_server_exceptions=True,
        ) as client:
            if consumer_fails:
                with pytest.raises(SyntheticConsumerError) as caught:
                    client.get("/probe")
                assert caught.value is failure
            else:
                response = client.get("/probe")
                assert response.status_code == 200
                assert response.json() == {"value": 1}

        assert len(sessions) == 1
        assert consumer_checkouts == [1]
        close_spies[0].assert_called_once_with()
        assert not sessions[0].in_transaction()
        assert synthetic_engine.pool.checkedout() == 0

        # A real subsequent checkout must succeed with no overflow allowed.
        with synthetic_engine.connect() as connection:
            assert connection.scalar(text("SELECT 1")) == 1
    finally:
        # Cleanup remains effective if an assertion above fails.
        for session in sessions:
            session.close()
