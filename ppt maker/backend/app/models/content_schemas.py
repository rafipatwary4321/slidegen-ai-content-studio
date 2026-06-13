from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

AspectRatioType = Literal["1:1", "4:5", "16:9", "9:16", "A4"]
WorkflowType = Literal["prompt", "template", "upload"]
LanguageType = Literal["en", "es", "fr", "de", "ar", "hi", "bn", "pt"]
ExportFormatType = Literal["png", "jpg", "pdf", "pptx", "zip"]


class BrandKitModel(BaseModel):
    name: str = "My Brand"
    primaryColor: str = "#8B5CF6"
    secondaryColor: str = "#22D3EE"
    accentColor: str = "#F472B6"
    fontHeading: str = "Inter"
    fontBody: str = "Inter"
    logoUrl: str | None = None


class CanvasLayerModel(BaseModel):
    id: str
    type: Literal["text", "image", "shape", "group"] = "text"
    name: str
    x: float = 0
    y: float = 0
    width: float = 100
    height: float = 40
    rotation: float = 0
    opacity: float = 1
    visible: bool = True
    locked: bool = False
    content: str | None = None
    fill: str | None = None
    zIndex: int = 0


class ContentGenerateRequest(BaseModel):
    category_id: str = Field(..., min_length=1)
    prompt: str = Field(..., min_length=1, max_length=2000)
    aspect_ratio: AspectRatioType = "16:9"
    language: LanguageType = "en"
    workflow: WorkflowType = "prompt"
    template_id: str | None = None
    brand_kit: BrandKitModel | None = None
    document_text: str | None = None


class StudioProjectModel(BaseModel):
    id: str
    category_id: str
    title: str
    aspect_ratio: AspectRatioType
    language: LanguageType
    workflow: WorkflowType
    template_id: str | None = None
    prompt: str
    layers: list[CanvasLayerModel]
    created_at: str
    updated_at: str
    recommended_exports: list[ExportFormatType] = Field(default_factory=list)


class ContentExportRequest(BaseModel):
    project_id: str
    format: ExportFormatType
    title: str = "Design"
    aspect_ratio: AspectRatioType = "16:9"
    layers: list[CanvasLayerModel] = Field(default_factory=list)


class ContentExportResponse(BaseModel):
    success: bool
    message: str
    download_url: str | None = None


class ContentGenerateResponse(BaseModel):
    success: bool
    message: str
    project: StudioProjectModel


class IntentClassifyRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)


class GenerationParametersModel(BaseModel):
    refined_prompt: str
    title: str | None = None
    quantity: int | None = None
    aspect_ratio: AspectRatioType | None = None
    language: LanguageType = "en"


class IntentAlternativeModel(BaseModel):
    category_id: str
    category_name: str
    confidence: float = Field(ge=0, le=1)


class IntentClassifyResponse(BaseModel):
    success: bool
    category_id: str
    category_name: str
    confidence: float = Field(ge=0, le=1)
    reasoning: str
    requires_manual_selection: bool
    parameters: GenerationParametersModel
    alternatives: list[IntentAlternativeModel] = Field(default_factory=list)


class PromptToDesignRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)
    category_id: str | None = None
    parameters: GenerationParametersModel | None = None
    brand_kit: BrandKitModel | None = None


class PromptToDesignResponse(BaseModel):
    success: bool
    message: str
    classification: IntentClassifyResponse
    project: StudioProjectModel | None = None
