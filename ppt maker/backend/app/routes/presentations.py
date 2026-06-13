from fastapi import APIRouter, HTTPException, status

from app.models.schemas import (
    ListPresentationsResponse,
    PresentationRecord,
    SavePresentationRequest,
    SavePresentationResponse,
)
from app.services.persistence import store

router = APIRouter()


@router.post("/presentations", response_model=SavePresentationResponse)
def save_presentation(payload: SavePresentationRequest) -> SavePresentationResponse:
    saved = store.save_presentation(payload)
    return SavePresentationResponse(success=True, message="Presentation saved.", presentation=saved)


@router.get("/presentations", response_model=ListPresentationsResponse)
def list_presentations(user_id: str | None = None) -> ListPresentationsResponse:
    return ListPresentationsResponse(success=True, presentations=store.list_presentations(user_id=user_id))


@router.get("/presentations/{presentation_id}", response_model=PresentationRecord)
def get_presentation(presentation_id: str, user_id: str | None = None) -> PresentationRecord:
    record = store.get_presentation(presentation_id, user_id=user_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presentation not found.")
    return record


@router.post("/presentations/{presentation_id}/regenerate", response_model=SavePresentationResponse)
def regenerate_presentation(presentation_id: str, user_id: str | None = None) -> SavePresentationResponse:
    record = store.regenerate_presentation(presentation_id, user_id=user_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Presentation not found.")
    return SavePresentationResponse(success=True, message="Presentation regenerated.", presentation=record)
