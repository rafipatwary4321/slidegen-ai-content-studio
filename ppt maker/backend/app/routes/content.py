from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.models.content_schemas import (
    ContentExportRequest,
    ContentExportResponse,
    ContentGenerateRequest,
    ContentGenerateResponse,
    IntentClassifyRequest,
    IntentClassifyResponse,
    PromptToDesignRequest,
    PromptToDesignResponse,
)
from app.services.content_export_service import EXPORT_DIR, ContentExportService
from app.services.content_generation_service import ContentGenerationService
from app.services.prompt_to_design_service import PromptToDesignService

router = APIRouter()
generator = ContentGenerationService()
exporter = ContentExportService()
prompt_to_design = PromptToDesignService()


@router.post("/content/classify-intent", response_model=IntentClassifyResponse)
def classify_intent(payload: IntentClassifyRequest) -> IntentClassifyResponse:
    return prompt_to_design.classify_only(payload.prompt)


@router.post("/content/prompt-to-design", response_model=PromptToDesignResponse)
def run_prompt_to_design(payload: PromptToDesignRequest) -> PromptToDesignResponse:
    return prompt_to_design.run(payload)


@router.post("/content/generate", response_model=ContentGenerateResponse)
def generate_content(payload: ContentGenerateRequest) -> ContentGenerateResponse:
    project = generator.generate(payload)
    return ContentGenerateResponse(success=True, message="Design generated.", project=project)


@router.post("/content/export", response_model=ContentExportResponse)
def export_content(payload: ContentExportRequest) -> ContentExportResponse:
    return exporter.export(payload)


@router.get("/content/download/{filename}")
def download_studio_export(filename: str):
    path = EXPORT_DIR / filename
    if not path.is_file():
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Export not found")
    return FileResponse(path, filename=filename)
