from app.schemas.work_items import (
    WorkItemClassification,
    WorkItemClassificationInput,
    WorkItemPriority,
    WorkItemType,
)

TYPE_RULES: tuple[tuple[WorkItemType, tuple[str, ...]], ...] = (
    (
        WorkItemType.INCIDENT,
        ("incident", "outage", "down", "unavailable", "service failure"),
    ),
    (
        WorkItemType.BUG,
        ("bug", "error", "exception", "crash", "defect", "broken"),
    ),
    (
        WorkItemType.RESEARCH,
        ("research", "investigate", "study", "analyze", "analysis"),
    ),
    (
        WorkItemType.IMPROVEMENT,
        ("improve", "enhance", "optimize", "refactor", "cleanup"),
    ),
    (
        WorkItemType.OPERATION,
        ("deploy", "backup", "monitor", "maintenance", "runbook"),
    ),
)

PRIORITY_RULES: tuple[tuple[WorkItemPriority, tuple[str, ...]], ...] = (
    (
        WorkItemPriority.CRITICAL,
        ("critical", "urgent", "outage", "production down", "unavailable"),
    ),
    (
        WorkItemPriority.HIGH,
        ("high", "important", "blocked", "failure", "crash"),
    ),
    (
        WorkItemPriority.LOW,
        ("low", "minor", "typo", "cosmetic"),
    ),
)


def classify_work_item(payload: WorkItemClassificationInput) -> WorkItemClassification:
    text = _combined_text(payload)
    reasons: list[str] = []

    suggested_type = WorkItemType.TASK
    for item_type, keywords in TYPE_RULES:
        matched_keyword = _first_match(text, keywords)
        if matched_keyword:
            suggested_type = item_type
            reasons.append(f"type matched keyword: {matched_keyword}")
            break

    suggested_priority = WorkItemPriority.MEDIUM
    for priority, keywords in PRIORITY_RULES:
        matched_keyword = _first_match(text, keywords)
        if matched_keyword:
            suggested_priority = priority
            reasons.append(f"priority matched keyword: {matched_keyword}")
            break

    if not reasons:
        reasons.append("default classification applied")

    suggested_tags = _suggest_tags(payload.tags, suggested_type, suggested_priority)

    return WorkItemClassification(
        suggested_type=suggested_type,
        suggested_priority=suggested_priority,
        suggested_tags=suggested_tags,
        reasons=reasons,
    )


def _combined_text(payload: WorkItemClassificationInput) -> str:
    parts = [payload.title, payload.description, *payload.tags]
    return " ".join(parts).lower()


def _first_match(text: str, keywords: tuple[str, ...]) -> str | None:
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None


def _suggest_tags(
    tags: list[str],
    suggested_type: WorkItemType,
    suggested_priority: WorkItemPriority,
) -> list[str]:
    normalized_tags = [tag.strip().lower() for tag in tags if tag.strip()]
    suggestions = [*normalized_tags, suggested_type.value]

    if suggested_priority in {WorkItemPriority.HIGH, WorkItemPriority.CRITICAL}:
        suggestions.append(suggested_priority.value)

    return list(dict.fromkeys(suggestions))
