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
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    status: WorkItemStatus = WorkItemStatus.OPEN
    priority: WorkItemPriority = WorkItemPriority.MEDIUM
    type: WorkItemType = WorkItemType.TASK
    source: WorkItemSource = WorkItemSource.MANUAL
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] | None = None


class WorkItemCreate(WorkItemBase):
    pass


class WorkItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: WorkItemStatus | None = None
    priority: WorkItemPriority | None = None
    type: WorkItemType | None = None
    source: WorkItemSource | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class WorkItemRead(WorkItemBase):
    id: int
    metadata: dict[str, Any] | None = Field(
        default=None,
        validation_alias="metadata_json",
    )
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
