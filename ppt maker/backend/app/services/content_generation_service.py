"""Shared layer-building logic for all content categories."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.models.content_schemas import BrandKitModel, CanvasLayerModel, ContentGenerateRequest, StudioProjectModel
from app.services.content.categories import get_category_spec
from app.services.openai_service import OpenAIService

ASPECT_DIMS = {
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "A4": (2480, 3508),
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fallback_layers(title: str, prompt: str, brand: BrandKitModel | None, w: int, h: int) -> list[CanvasLayerModel]:
    primary = brand.primaryColor if brand else "#8B5CF6"
    return [
        CanvasLayerModel(
            id=str(uuid4()),
            type="shape",
            name="Background",
            x=0,
            y=0,
            width=w,
            height=h,
            fill=primary,
            zIndex=0,
        ),
        CanvasLayerModel(
            id=str(uuid4()),
            type="text",
            name="Headline",
            x=w * 0.08,
            y=h * 0.12,
            width=w * 0.84,
            height=h * 0.2,
            content=title,
            zIndex=1,
        ),
        CanvasLayerModel(
            id=str(uuid4()),
            type="text",
            name="Body",
            x=w * 0.08,
            y=h * 0.38,
            width=w * 0.84,
            height=h * 0.4,
            content=prompt[:500],
            zIndex=2,
        ),
    ]


class ContentGenerationService:
    """Unified prompt / template / upload → canvas project pipeline."""

    def __init__(self) -> None:
        self._openai = OpenAIService()

    def generate(self, request: ContentGenerateRequest) -> StudioProjectModel:
        if request.category_id == "presentations" and request.workflow == "upload" and request.document_text:
            return self._presentation_from_document(request)

        spec = get_category_spec(request.category_id)
        w, h = ASPECT_DIMS.get(request.aspect_ratio, (1920, 1080))
        title, layers = self._ai_design_layers(request, spec, w, h)
        now = _now()
        return StudioProjectModel(
            id=str(uuid4()),
            category_id=request.category_id,
            title=title,
            aspect_ratio=request.aspect_ratio,
            language=request.language,
            workflow=request.workflow,
            template_id=request.template_id,
            prompt=request.prompt,
            layers=layers,
            created_at=now,
            updated_at=now,
            recommended_exports=list(spec.exports),
        )

    def _ai_design_layers(
        self,
        request: ContentGenerateRequest,
        spec,
        w: int,
        h: int,
    ) -> tuple[str, list[CanvasLayerModel]]:
        brand = request.brand_kit or BrandKitModel()
        if not self._openai.enabled:
            title = request.prompt[:80] or spec.name
            return title, _fallback_layers(title, request.prompt, brand, w, h)

        system = f"""You are a senior visual designer for {spec.name}.
Return ONLY JSON: {{ "title": string, "layers": [ {{ "type": "text"|"shape", "name": string, "x": number, "y": number, "width": number, "height": number, "content": string?, "fill": string?, "zIndex": number }} ] }}
Canvas: {w}x{h}. Aspect: {request.aspect_ratio}. Language: {request.language}.
Brand primary: {brand.primaryColor}. Hint: {spec.system_hint}.
Keep text concise. Max 8 layers."""

        user = f"Workflow: {request.workflow}. Template: {request.template_id or 'none'}.\nPrompt: {request.prompt}"
        if request.document_text:
            user += f"\nSource text:\n{request.document_text[:8000]}"

        raw = self._openai._chat_json(system, user, max_tokens=4096)
        if raw and isinstance(raw.get("layers"), list):
            title = str(raw.get("title", request.prompt[:80]))
            layers: list[CanvasLayerModel] = []
            for i, item in enumerate(raw["layers"][:12]):
                if not isinstance(item, dict):
                    continue
                layers.append(
                    CanvasLayerModel(
                        id=str(uuid4()),
                        type=item.get("type", "text") if item.get("type") in ("text", "shape", "image", "group") else "text",
                        name=str(item.get("name", f"Layer {i+1}")),
                        x=float(item.get("x", 0)),
                        y=float(item.get("y", 0)),
                        width=float(item.get("width", 100)),
                        height=float(item.get("height", 40)),
                        content=str(item.get("content", "")) if item.get("content") else None,
                        fill=str(item.get("fill", brand.primaryColor)) if item.get("fill") else None,
                        zIndex=int(item.get("zIndex", i)),
                    )
                )
            if layers:
                return title, layers

        title = request.prompt[:80] or spec.name
        return title, _fallback_layers(title, request.prompt, brand, w, h)

    def _presentation_from_document(self, request: ContentGenerateRequest) -> StudioProjectModel:
        from app.services.ai_orchestration import AIOrchestrationService

        ai = AIOrchestrationService()
        analysis = ai.analyze_document(request.document_text or "", "upload.txt")
        w, h = ASPECT_DIMS["16:9"]
        brand = request.brand_kit or BrandKitModel()
        layers: list[CanvasLayerModel] = [
            CanvasLayerModel(
                id=str(uuid4()),
                type="text",
                name=f"Slide {s.slide_number}",
                x=80,
                y=80 + (i * 120) % int(h * 0.7),
                width=w - 160,
                height=100,
                content=f"{s.title}: " + "; ".join(s.bullets[:3]),
                zIndex=i,
            )
            for i, s in enumerate(analysis.outline[:10])
        ]
        now = _now()
        return StudioProjectModel(
            id=str(uuid4()),
            category_id="presentations",
            title=analysis.presentation_title,
            aspect_ratio="16:9",
            language=request.language,
            workflow=request.workflow,
            template_id=request.template_id,
            prompt=request.prompt,
            layers=layers or _fallback_layers(analysis.presentation_title, analysis.summary, brand, w, h),
            created_at=now,
            updated_at=now,
            recommended_exports=["pptx", "pdf", "png", "zip"],
        )
