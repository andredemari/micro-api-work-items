from app.schemas.work_items import (
    WorkItemClassificationInput,
    WorkItemPriority,
    WorkItemType,
)
from app.services.classifier import classify_work_item


def test_classifier_defaults_to_task_and_medium_without_keywords() -> None:
    result = classify_work_item(
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


def test_classifier_detects_bug_and_high_priority() -> None:
    result = classify_work_item(
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


def test_classifier_normalizes_and_deduplicates_tags() -> None:
    result = classify_work_item(
        WorkItemClassificationInput(
            title="Investigate low priority cleanup",
            description="",
            tags=[" Research ", "research", "LOW", ""],
        )
    )

    assert result.suggested_type == WorkItemType.RESEARCH
    assert result.suggested_priority == WorkItemPriority.LOW
    assert result.suggested_tags == ["research", "low"]
