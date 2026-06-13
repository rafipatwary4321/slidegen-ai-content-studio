"""
PPTX export job runner.

Today: synchronous export in the API request.
Future: set EXPORT_ASYNC=true and enqueue via Celery/RQ (see enqueue_export stub).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from app.models.schemas import ExportPptxRequest, ExportResult
from app.services.pptx_service import PptxService


@dataclass
class ExportJobResult:
    export: ExportResult
    queued: bool = False
    job_id: str | None = None


class ExportJobService:
    def __init__(self) -> None:
        self._pptx = PptxService()
        self._async_enabled = os.getenv("EXPORT_ASYNC", "").lower() in ("1", "true", "yes")

    def run(self, payload: ExportPptxRequest) -> ExportJobResult:
        if self._async_enabled:
            job_id = self.enqueue_export(payload)
            raise NotImplementedError(
                f"Async export job {job_id} queued — wire Celery/RQ worker to process ExportPptxRequest."
            )
        export = self._pptx.export(
            title=payload.title,
            slides=payload.slides,
            theme=payload.theme,
            speaker_notes=payload.speaker_notes,
        )
        return ExportJobResult(export=export, queued=False)

    def enqueue_export(self, payload: ExportPptxRequest) -> str:
        """Stub for background worker integration."""
        from uuid import uuid4

        job_id = str(uuid4())
        # Future: celery_app.send_task("slidegen.export_pptx", args=[payload.model_dump(), job_id])
        _ = payload
        return job_id

    def resolve_export_path(self, export_id: str):
        return self._pptx.resolve_export_path(export_id)
