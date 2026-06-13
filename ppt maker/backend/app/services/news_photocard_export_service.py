"""News photocard export — manifest registry for future server-side raster pipeline."""

from __future__ import annotations

import json
from uuid import uuid4

from app.models.news_photocard_schemas import NewsPhotocardExportRequest, NewsPhotocardExportResponse
from app.services.content_export_service import EXPORT_DIR


class NewsPhotocardExportService:
    """Client renders real PNG today; server stores export manifests for future Pillow/headless rendering."""

    def register_export(self, request: NewsPhotocardExportRequest) -> NewsPhotocardExportResponse:
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        export_id = str(uuid4())
        manifest = {
            "exportId": export_id,
            "format": "png",
            "renderer": "client-canvas",
            "serverRaster": False,
            "headline": request.headline,
            "subheadline": request.subheadline,
            "category": request.category,
            "aspectRatio": request.aspect_ratio,
            "tone": request.tone,
            "designStyle": request.design_style,
            "language": request.language,
            "hasLogo": request.has_logo,
            "hasImage": request.has_image,
            "note": "PNG delivered by browser canvas export. Server raster hook reserved.",
        }
        filename = f"news-photocard-{export_id[:8]}.json"
        path = EXPORT_DIR / filename
        path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return NewsPhotocardExportResponse(
            success=True,
            message="Export manifest registered. PNG is generated client-side.",
            export_id=export_id,
            manifest_url=f"/api/v1/content/download/{filename}",
            server_png_ready=False,
        )
