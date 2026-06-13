"""Prompt-to-design orchestration: classify intent → route → generate."""

from __future__ import annotations

from app.models.content_schemas import (
    ContentGenerateRequest,
    GenerationParametersModel,
    IntentClassifyResponse,
    PromptToDesignRequest,
    PromptToDesignResponse,
)
from app.services.content.categories import get_category_spec
from app.services.content_generation_service import ContentGenerationService
from app.services.intent_classifier import IntentClassifierService


class PromptToDesignService:
    def __init__(self) -> None:
        self._classifier = IntentClassifierService()
        self._generator = ContentGenerationService()

    def run(self, request: PromptToDesignRequest) -> PromptToDesignResponse:
        classification = self._resolve_classification(request)

        if classification.requires_manual_selection and not request.category_id:
            return PromptToDesignResponse(
                success=True,
                message="Low confidence — please confirm or choose a category.",
                classification=classification,
                project=None,
            )

        category_id = request.category_id or classification.category_id
        params = request.parameters or classification.parameters
        spec = get_category_spec(category_id)

        gen_prompt = params.refined_prompt or request.prompt
        if params.quantity and params.quantity > 1:
            gen_prompt = f"{gen_prompt}\n\nBulk batch: generate {params.quantity} variants for participants."

        aspect = params.aspect_ratio or spec.default_aspect
        if aspect not in ("1:1", "4:5", "16:9", "9:16", "A4"):
            aspect = spec.default_aspect

        generate_req = ContentGenerateRequest(
            category_id=category_id,
            prompt=gen_prompt,
            aspect_ratio=aspect,
            language=params.language,
            workflow="prompt",
            brand_kit=request.brand_kit,
        )
        project = self._generator.generate(generate_req)

        return PromptToDesignResponse(
            success=True,
            message=f"Generated {spec.name} design.",
            classification=classification,
            project=project,
        )

    def classify_only(self, prompt: str) -> IntentClassifyResponse:
        return self._classifier.classify(prompt)

    def _resolve_classification(self, request: PromptToDesignRequest) -> IntentClassifyResponse:
        if request.category_id and request.parameters:
            spec = get_category_spec(request.category_id)
            return IntentClassifyResponse(
                success=True,
                category_id=spec.id,
                category_name=spec.name,
                confidence=1.0,
                reasoning="Category selected by user.",
                requires_manual_selection=False,
                parameters=request.parameters,
                alternatives=[],
            )
        if request.category_id:
            base = self._classifier.classify(request.prompt)
            spec = get_category_spec(request.category_id)
            return IntentClassifyResponse(
                success=True,
                category_id=spec.id,
                category_name=spec.name,
                confidence=1.0,
                reasoning="Category confirmed by user.",
                requires_manual_selection=False,
                parameters=base.parameters,
                alternatives=base.alternatives,
            )
        return self._classifier.classify(request.prompt)
