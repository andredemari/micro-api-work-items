import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.db.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import work_item_model  # noqa: E402,F401

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    expire_on_commit=False,
)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide an isolated in-memory database session for service tests."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient wired to the isolated in-memory database."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        test_client.close()

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def record_observation(tmp_path, request):
    """Write observations outside the public source tree; not product acceptance."""
    from datetime import datetime, timezone
    import json
    from pathlib import Path
    import uuid

    def record(case_id, data):
        destination = Path(os.environ.get("EXTENSION_EVIDENCE", str(tmp_path / "observations")))
        destination.mkdir(parents=True, exist_ok=True)
        value = {
            "case_id": case_id, "nodeid": request.node.nodeid,
            "oracle_status": "observed-not-product-approval",
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(), "data": data,
        }
        path = destination / (case_id + "-" + uuid.uuid4().hex[:10] + ".json")
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return value

    return record


@pytest.fixture()
def http_process(tmp_path, record_observation):
    from http_process_support import HttpProcess

    process = HttpProcess(tmp_path / "http", record_observation)
    try:
        yield process
    finally:
        process.stop()
