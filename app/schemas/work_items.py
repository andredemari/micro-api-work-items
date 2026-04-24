from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkItemStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


class WorkItemPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkItemType(str, Enum):
    TASK = "task"
    BUG = "bug"
    IMPROVEMENT = "improvement"
    RESEARCH = "research"
    OPERATION = "operation"
    INCIDENT = "incident"


class WorkItemSource(str, Enum):
    MANUAL = "manual"
    SYSTEM = "system"
    OTHER = "other"


class WorkItemBase(BaseModel):
    """Shared API contract for work item create and read operations."""

    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    status: WorkItemStatus = WorkItemStatus.OPEN
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    type: WorkItemType = WorkItemType.TASK
    source: WorkItemSource = WorkItemSource.MANUAL
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] | None = None


class WorkItemCreate(WorkItemBase):
    """Request body for creating a persisted work item."""

    pass


class WorkItemUpdate(BaseModel):
    """Request body for partially updating a persisted work item."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    type: WorkItemType | None = None
    source: WorkItemSource | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class WorkItemRead(WorkItemBase):
    """Response schema for a persisted work item."""

    id: int
    metadata: dict[str, Any] | None = Field(
        default=None,
        validation_alias="metadata_json",
    )
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkItemClassificationInput(BaseModel):
    """Input schema for side-effect-free local classification."""

    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    tags: list[str] = Field(default_factory=list)


class WorkItemClassification(BaseModel):
    """Suggested type, priority, tags, and reasons from local rules."""

    suggested_type: WorkItemType
    suggested_priority: WorkItemPriority
    suggested_tags: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
