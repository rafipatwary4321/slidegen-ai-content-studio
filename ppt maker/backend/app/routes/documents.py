from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.schemas import AnalyzeDocumentResponse
from app.services.ai_orchestration import AIOrchestrationService
from app.services.file_parser_service import FileParserService
from app.services.persistence import store
from app.services.storage_service import store_upload_blob
from app.utils.file_helpers import MAX_UPLOAD_BYTES, get_extension

router = APIRouter()
ai = AIOrchestrationService()
parser_service = FileParserService()


@router.post("/documents/analyze", response_model=AnalyzeDocumentResponse)
async def analyze_document(file: UploadFile = File(...)) -> AnalyzeDocumentResponse:
    if not parser_service.is_supported_filename(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Allowed: PDF, DOCX, TXT.",
        )

    try:
        file_bytes = await file.read()
        if len(file_bytes) > MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds 25MB limit.",
            )
        store_upload_blob(file.filename or "upload", file_bytes, file.content_type or "application/octet-stream")
        parsed = parser_service.parse_document(file.filename, file.content_type, file_bytes)
        store.save_uploaded_file_metadata(parsed.metadata, status="analyzed")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    result = ai.analyze_document(parsed.prepared_text, parsed.metadata.filename)
    return AnalyzeDocumentResponse(
        success=True,
        message="Document analyzed.",
        parsed_document=parsed,
        analysis=result,
    )
