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
