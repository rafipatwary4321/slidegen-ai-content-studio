from fastapi import APIRouter

from app.models.schemas import (
    GenerateOutlineRequest,
    GenerateOutlineResponse,
    ReviseOutlineRequest,
    ReviseOutlineResponse,
)
from app.services.ai_orchestration import AIOrchestrationService
from app.services.persistence import store

router = APIRouter()
ai = AIOrchestrationService()


@router.post("/outlines/generate", response_model=GenerateOutlineResponse)
def generate_outline(payload: GenerateOutlineRequest) -> GenerateOutlineResponse:
    outline = ai.generate_outline(payload)
    return GenerateOutlineResponse(success=True, message="Outline generated.", outline=outline)


@router.post("/outlines/revise", response_model=ReviseOutlineResponse)
def revise_outline(payload: ReviseOutlineRequest) -> ReviseOutlineResponse:
    updated = ai.revise_outline(payload)
    if payload.presentation_id:
        store.save_revision_prompt(
            presentation_id=payload.presentation_id,
            instruction=payload.instruction,
            previous_outline=payload.outline,
            updated_outline=updated,
            user_id=payload.user_id,
        )
    return ReviseOutlineResponse(
        success=True,
        message="Outline revised.",
        previous_outline=payload.outline,
        updated_outline=updated,
    )
