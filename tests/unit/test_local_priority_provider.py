import pytest

from app.providers.priority.local_provider import suggest_work_item_classification
from app.schemas.work_items import (
    WorkItemClassificationInput,
    WorkItemPriority,
    WorkItemType,
)


def test_local_provider_defaults_to_task_and_medium_without_keywords() -> None:
    result = suggest_work_item_classification(
        WorkItemClassificationInput(
            title="Plan weekly notes",
            description="Organize a short update.",
            tags=[],
        )
    )

    assert result.suggested_type == WorkItemType.TASK
    assert result.suggested_priority == WorkItemPriority.MEDIUM
    assert result.suggested_tags == ["task"]
    assert result.reasons == ["default classification applied"]


def test_local_provider_detects_bug_and_high_priority() -> None:
    result = suggest_work_item_classification(
        WorkItemClassificationInput(
            title="Fix crash in workflow",
            description="High priority failure during execution.",
            tags=["Backend"],
        )
    )

    assert result.suggested_type == WorkItemType.BUG
    assert result.suggested_priority == WorkItemPriority.HIGH
    assert result.suggested_tags == ["backend", "bug", "high"]
    assert result.reasons == [
        "type matched keyword: crash",
        "priority matched keyword: high",
    ]


def test_local_provider_detects_critical_incident() -> None:
    result = suggest_work_item_classification(
        WorkItemClassificationInput(
            title="Critical incident",
            description="Service unavailable for users.",
            tags=["Ops"],
        )
    )

    assert result.suggested_type == WorkItemType.INCIDENT
    assert result.suggested_priority == WorkItemPriority.CRITICAL
    assert result.suggested_tags == ["ops", "incident", "critical"]
    assert result.reasons == [
        "type matched keyword: incident",
        "priority matched keyword: critical",
    ]


def test_local_provider_normalizes_and_deduplicates_tags() -> None:
    result = suggest_work_item_classification(
        WorkItemClassificationInput(
            title="Investigate low priority cleanup",
            description="",
            tags=[" Research ", "research", "LOW", ""],
        )
    )

    assert result.suggested_type == WorkItemType.RESEARCH
    assert result.suggested_priority == WorkItemPriority.LOW
    assert result.suggested_tags == ["research", "low"]


pytestmark = [pytest.mark.unit]


# CLS-INPUT: side-effect invariant; does not establish keyword precedence.
def test_classification_preserves_input_model_and_tags() -> None:
    payload = WorkItemClassificationInput(
        title="Research crash", description="urgent backup",
        tags=[" HIGH ", "high", "", "Ops"],
    )
    before = payload.model_dump(mode="json")

    suggest_work_item_classification(payload)

    assert payload.model_dump(mode="json") == before


# CLS-ALIAS: results must not share mutable tag state with inputs or each other.
def test_suggested_tags_do_not_alias_input_or_other_results() -> None:
    payload = WorkItemClassificationInput(title="Plan notes", tags=[" Notes "])
    before = payload.model_dump(mode="json")
    first = suggest_work_item_classification(payload)
    second = suggest_work_item_classification(payload)
    expected = second.model_dump(mode="json")

    first.suggested_tags.append("synthetic-client-edit")
    first.reasons.append("synthetic-client-edit")

    assert payload.model_dump(mode="json") == before
    assert second.model_dump(mode="json") == expected
    assert suggest_work_item_classification(payload).model_dump(mode="json") == expected
