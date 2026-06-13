"""Poster export — manifest registry for future server-side raster pipeline."""

from __future__ import annotations

import json
from uuid import uuid4

from app.models.poster_schemas import PosterExportRequest, PosterExportResponse
from app.services.content_export_service import EXPORT_DIR


class PosterExportService:
    """Client renders real PNG today; server stores export manifests for future Pillow/headless rendering."""

    def register_export(self, request: PosterExportRequest) -> PosterExportResponse:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        export_id = str(uuid4())
        manifest = {
            "exportId": export_id,
            "format": "png",
            "renderer": "client-canvas",
            "serverRaster": False,
            "title": request.title,
            "subtitle": request.subtitle,
            "posterType": request.poster_type,
            "aspectRatio": request.aspect_ratio,
            "designTone": request.design_tone,
            "language": request.language,
            "dateTime": request.date_time,
            "venue": request.venue,
            "organizer": request.organizer,
            "ctaText": request.cta_text,
            "hasLogo": request.has_logo,
            "hasImage": request.has_image,
            "note": "PNG delivered by browser canvas export. Server raster hook reserved.",
        }
        filename = f"poster-{export_id[:8]}.json"
        path = EXPORT_DIR / filename
        path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return PosterExportResponse(
            success=True,
            message="Export manifest registered. PNG is generated client-side.",
            export_id=export_id,
            manifest_url=f"/api/v1/content/download/{filename}",
            server_png_ready=False,
        )
