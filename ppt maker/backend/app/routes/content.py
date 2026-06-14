from fastapi import APIRouter, HTTPException
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
from app.models.news_photocard_schemas import (
    NewsPhotocardAiCopyRequest,
    NewsPhotocardAiCopyResponse,
    NewsPhotocardExportRequest,
    NewsPhotocardExportResponse,
    NewsPhotocardGenerateRequest,
    NewsPhotocardGenerateResponse,
)
from app.models.poster_schemas import (
    PosterAiCopyRequest,
    PosterAiCopyResponse,
    PosterExportRequest,
    PosterExportResponse,
    PosterGenerateRequest,
    PosterGenerateResponse,
)
from app.services.content_export_service import EXPORT_DIR, ContentExportService
from app.services.content_generation_service import ContentGenerationService
from app.services.news_photocard_export_service import NewsPhotocardExportService
from app.services.news_photocard_service import NewsPhotocardService
from app.services.poster_export_service import PosterExportService
from app.services.poster_service import PosterService
from app.services.prompt_to_design_service import PromptToDesignService

router = APIRouter()
generator = ContentGenerationService()
exporter = ContentExportService()
prompt_to_design = PromptToDesignService()
news_photocard = NewsPhotocardService()
news_photocard_export = NewsPhotocardExportService()
poster = PosterService()
poster_export = PosterExportService()


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


@router.post("/content/generate/news-photocard", response_model=NewsPhotocardGenerateResponse)
def generate_news_photocard(payload: NewsPhotocardGenerateRequest) -> NewsPhotocardGenerateResponse:
    try:
        return news_photocard.generate(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/content/generate/news-photocard/ai-copy", response_model=NewsPhotocardAiCopyResponse)
def generate_news_photocard_ai_copy(payload: NewsPhotocardAiCopyRequest) -> NewsPhotocardAiCopyResponse:
    return news_photocard.generate_copy(payload)


@router.post("/content/export/news-photocard", response_model=NewsPhotocardExportResponse)
def register_news_photocard_export(payload: NewsPhotocardExportRequest) -> NewsPhotocardExportResponse:
    return news_photocard_export.register_export(payload)


@router.post("/content/generate/poster", response_model=PosterGenerateResponse)
def generate_poster(payload: PosterGenerateRequest) -> PosterGenerateResponse:
    try:
        return poster.generate(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/content/generate/poster/ai-copy", response_model=PosterAiCopyResponse)
def generate_poster_ai_copy(payload: PosterAiCopyRequest) -> PosterAiCopyResponse:
    return poster.generate_copy(payload)


@router.post("/content/export/poster", response_model=PosterExportResponse)
def register_poster_export(payload: PosterExportRequest) -> PosterExportResponse:
    return poster_export.register_export(payload)


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
