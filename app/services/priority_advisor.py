from app.providers.priority.local_provider import suggest_work_item_classification
from app.schemas.work_items import WorkItemClassification, WorkItemClassificationInput


def advise_work_item(payload: WorkItemClassificationInput) -> WorkItemClassification:
    """Suggest work item classification using deterministic PriorityAdvisor rules."""
    return suggest_work_item_classification(payload)
