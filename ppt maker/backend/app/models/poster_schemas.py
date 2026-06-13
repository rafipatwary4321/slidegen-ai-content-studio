from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

PosterTypeId = Literal["event", "political", "educational", "business", "awareness", "product"]
PosterLanguageType = Literal["en", "bn"]
PosterAspectRatioType = Literal["1:1", "4:5", "9:16", "A4"]
PosterDesignToneType = Literal[
    "premium-corporate",
    "bold-political",
    "modern-youth",
    "academic-clean",
    "luxury-event",
]


class PosterGenerateRequest(BaseModel):
    title: str = Field(default="", max_length=200)
    subtitle: str = Field(default="", max_length=300)
    poster_type: PosterTypeId = "event"
    date_time: str | None = Field(default=None, max_length=120)
    venue: str | None = Field(default=None, max_length=200)
    organizer: str | None = Field(default=None, max_length=120)
    cta_text: str = Field(default="Learn More", max_length=80)
    language: PosterLanguageType = "en"
    aspect_ratio: PosterAspectRatioType = "A4"
    design_tone: PosterDesignToneType = "luxury-event"
    ai_prompt: str | None = Field(default=None, max_length=2000)
    has_logo: bool = False
    has_image: bool = False


class PosterData(BaseModel):
    title: str
    subtitle: str
    posterType: PosterTypeId
    language: PosterLanguageType
    aspectRatio: PosterAspectRatioType
    designTone: PosterDesignToneType
    layoutInstructions: str
    exportReadyData: dict[str, Any]


class PosterGenerateResponse(BaseModel):
    success: bool
    message: str
    data: PosterData


class PosterAiCopyRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)
    language: PosterLanguageType = "en"


class PosterAiCopyData(BaseModel):
    title: str
    subtitle: str
    ctaText: str
    posterType: PosterTypeId
    designTone: PosterDesignToneType
    layoutDirection: str
    source: Literal["openai", "mock"] = "mock"


class PosterAiCopyResponse(BaseModel):
    success: bool
    message: str
    data: PosterAiCopyData


class PosterExportRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    subtitle: str = Field(default="", max_length=300)
    poster_type: PosterTypeId = "event"
    aspect_ratio: PosterAspectRatioType = "A4"
    design_tone: PosterDesignToneType = "luxury-event"
    language: PosterLanguageType = "en"
    date_time: str | None = None
    venue: str | None = None
    organizer: str | None = None
    cta_text: str = "Learn More"
    has_logo: bool = False
    has_image: bool = False


class PosterExportResponse(BaseModel):
    success: bool
    message: str
    export_id: str
    manifest_url: str
    server_png_ready: bool = False
