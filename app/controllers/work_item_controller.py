from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.work_items import (
    WorkItemClassification,
    WorkItemClassificationInput,
    WorkItemCreate,
    WorkItemRead,
    WorkItemUpdate,
)
from app.services.classifier import classify_work_item as classify_work_item_service
from app.services import work_items as work_item_service

router = APIRouter(prefix="/work-items", tags=["work-items"])


@router.post("", response_model=WorkItemRead, status_code=status.HTTP_201_CREATED)
def create_work_item(
    payload: WorkItemCreate,
    db: Session = Depends(get_db),
) -> WorkItemRead:
    return work_item_service.create_work_item(db, payload)


@router.get("", response_model=list[WorkItemRead])
def list_work_items(db: Session = Depends(get_db)) -> list[WorkItemRead]:
    return work_item_service.list_work_items(db)


@router.post("/classify", response_model=WorkItemClassification)
def classify_work_item(
    payload: WorkItemClassificationInput,
) -> WorkItemClassification:
    return classify_work_item_service(payload)


@router.get("/{work_item_id}", response_model=WorkItemRead)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db),
) -> WorkItemRead:
    work_item = work_item_service.get_work_item(db, work_item_id)
    if work_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found.",
        )
    return work_item


@router.patch("/{work_item_id}", response_model=WorkItemRead)
def update_work_item(
    work_item_id: int,
    payload: WorkItemUpdate,
    db: Session = Depends(get_db),
) -> WorkItemRead:
    work_item = work_item_service.update_work_item(db, work_item_id, payload)
    if work_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found.",
        )
    return work_item


@router.delete("/{work_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_item(
    work_item_id: int,
    db: Session = Depends(get_db),
) -> Response:
    deleted = work_item_service.delete_work_item(db, work_item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work item not found.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
