from fastapi import APIRouter

from app.models.schemas import GenerateNotesRequest, GenerateNotesResponse
from app.services.ai_orchestration import AIOrchestrationService

router = APIRouter()
ai = AIOrchestrationService()


@router.post("/notes/generate", response_model=GenerateNotesResponse)
def generate_speaker_notes(payload: GenerateNotesRequest) -> GenerateNotesResponse:
    notes = ai.generate_speaker_notes(payload.slides)
    return GenerateNotesResponse(success=True, message="Speaker notes generated.", notes=notes)
