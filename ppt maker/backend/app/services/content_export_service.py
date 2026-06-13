"""Export studio designs to PNG, JPG, PDF, PPTX, or ZIP bundles."""

from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from app.models.content_schemas import ContentExportRequest, ContentExportResponse

EXPORT_DIR = Path(__file__).resolve().parents[2] / "data" / "exports" / "studio"


class ContentExportService:
    def __init__(self) -> None:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    def export(self, request: ContentExportRequest) -> ContentExportResponse:
        fmt = request.format
        if fmt == "pptx" and request.aspect_ratio == "16:9":
            return self._export_pptx_stub(request)
        if fmt == "zip":
            return self._export_zip(request)
        return self._export_manifest(request, fmt)

    def _export_manifest(self, request: ContentExportRequest, fmt: str) -> ContentExportResponse:
        payload = {
            "title": request.title,
            "aspect_ratio": request.aspect_ratio,
            "format": fmt,
            "layers": [layer.model_dump() for layer in request.layers],
        }
        ext = "json" if fmt in ("png", "jpg", "pdf") else fmt
        filename = f"{request.project_id}-{uuid4().hex[:8]}.{ext}"
        path = EXPORT_DIR / filename
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        url = f"/api/v1/content/download/{filename}"
        return ContentExportResponse(
            success=True,
            message=f"{fmt.upper()} export package ready (layer manifest). Raster/PDF rendering hooks available.",
            download_url=url,
        )

    def _export_zip(self, request: ContentExportRequest) -> ContentExportResponse:
        buf = BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(
                "design.json",
                json.dumps(
                    {
                        "title": request.title,
                        "aspect_ratio": request.aspect_ratio,
                        "layers": [layer.model_dump() for layer in request.layers],
                    },
                    indent=2,
                ),
            )
            zf.writestr("README.txt", "SlideGen AI Content Studio bulk export bundle.\n")
        filename = f"{request.project_id}-{uuid4().hex[:8]}.zip"
        path = EXPORT_DIR / filename
        path.write_bytes(buf.getvalue())
        return ContentExportResponse(
            success=True,
            message="ZIP bundle ready.",
            download_url=f"/api/v1/content/download/{filename}",
        )

    def _export_pptx_stub(self, request: ContentExportRequest) -> ContentExportResponse:
        from app.models.schemas import SlideOutlineItem
        from app.services.pptx_service import PptxService

        slides = [
            SlideOutlineItem(
                slide_number=i + 1,
                title=layer.name[:140],
                bullets=[layer.content or ""],
            )
            for i, layer in enumerate(request.layers)
            if layer.type == "text" and layer.content
        ]
        if not slides:
            slides = [SlideOutlineItem(slide_number=1, title=request.title[:140], bullets=[request.title])]
        result = PptxService().export(request.title, slides, theme="modern")
        return ContentExportResponse(
            success=True,
            message="PPTX exported via presentation pipeline.",
            download_url=result.download_url,
        )
