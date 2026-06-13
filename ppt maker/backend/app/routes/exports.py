from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.jobs.export_jobs import ExportJobService
from app.models.schemas import ExportPptxRequest, ExportPptxResponse
from app.services.persistence import store

router = APIRouter()
export_jobs = ExportJobService()


@router.post("/exports/pptx", response_model=ExportPptxResponse)
def export_pptx(payload: ExportPptxRequest) -> ExportPptxResponse:
    job = export_jobs.run(payload)
    export_result = job.export
    if payload.presentation_id:
        store.update_pptx_file_path(payload.presentation_id, export_result.file_path, user_id=payload.user_id)
        store.save_exported_file(payload.presentation_id, export_result, user_id=payload.user_id)
    return ExportPptxResponse(success=True, message="PPTX export prepared.", export=export_result)


@router.get("/exports/pptx/{export_id}/download")
def download_pptx(export_id: str) -> FileResponse:
    file_path = export_jobs.resolve_export_path(export_id)
    if file_path is None or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Export file not found.",
        )
    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename=file_path.name,
    )
