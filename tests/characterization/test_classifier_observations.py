"""Recorded implementation observations, not newly approved classifier policies."""
import hashlib
from pathlib import Path

import pytest
from app.providers.priority import local_provider
from app.schemas.work_items import WorkItemClassificationInput

pytestmark = [pytest.mark.unit, pytest.mark.characterization]

CASES = [
    ("OBS-CLS-CATEGORY", {"title": "bug incident"}),
    ("OBS-CLS-PRIORITY", {"title": "low high critical"}),
    ("OBS-CLS-TITLE", {"title": "bug"}),
    ("OBS-CLS-DESCRIPTION", {"title": "Plan notes", "description": "bug"}),
    ("OBS-CLS-TAGS", {"title": "Plan notes", "tags": ["bug"]}),
    ("OBS-CLS-LOWER", {"title": "bug", "tags": ["ops"]}),
    ("OBS-CLS-UPPER", {"title": "BUG", "tags": ["OPS"]}),
    ("OBS-CLS-ORDER", {"title": "critical incident", "tags": [" Beta ", "ALPHA", "beta", "", "alpha", "high", "HIGH"]}),
    ("OBS-CLS-SUBSTRING", {"title": "Download release notes"}),
]


@pytest.mark.parametrize("case_id, values", CASES, ids=[row[0] for row in CASES])
def test_classifier_observation(case_id, values, record_observation):
    payload = WorkItemClassificationInput(**values)
    before = payload.model_dump(mode="json")
    result = local_provider.suggest_work_item_classification(payload)
    record_observation(case_id, {
        "input_before": before, "input_after": payload.model_dump(mode="json"),
        "output": result.model_dump(mode="json"),
        "source_sha256": hashlib.sha256(Path(local_provider.__file__).read_bytes()).hexdigest(),
        "meaning": "Successful capture is not approval of precedence, normalization or substring policy.",
    })
