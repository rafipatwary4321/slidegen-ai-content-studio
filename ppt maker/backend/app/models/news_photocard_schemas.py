from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

NewsCategoryType = Literal["politics", "campus", "sports", "international", "business", "entertainment"]
NewsLanguageType = Literal["en", "bn"]
NewsAspectRatioType = Literal["1:1", "4:5", "9:16"]
NewsToneType = Literal["breaking-news", "premium-editorial", "youth-media", "corporate-press"]
NewsDesignStyleType = Literal["dark-red", "black", "white", "gold"]


class NewsPhotocardGenerateRequest(BaseModel):
    headline: str = Field(default="", max_length=200)
    subheadline: str = Field(default="", max_length=300)
    news_category: NewsCategoryType = "politics"
    language: NewsLanguageType = "en"
    aspect_ratio: NewsAspectRatioType = "4:5"
    tone: NewsToneType = "breaking-news"
    design_style: NewsDesignStyleType = "dark-red"
    ai_prompt: str | None = Field(default=None, max_length=2000)
    has_logo: bool = False
    has_image: bool = False


class NewsPhotocardAiCopyRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000)
    language: NewsLanguageType = "en"


class NewsPhotocardAiCopyData(BaseModel):
    headline: str
    subheadline: str
    category: NewsCategoryType
    tone: NewsToneType
    layoutDirection: str
    source: Literal["openai", "mock"] = "mock"


class NewsPhotocardAiCopyResponse(BaseModel):
    success: bool
    message: str
    data: NewsPhotocardAiCopyData


class NewsPhotocardData(BaseModel):
    title: str
    headline: str
    subheadline: str
    category: str
    language: NewsLanguageType
    aspectRatio: NewsAspectRatioType
    tone: NewsToneType
    designStyle: NewsDesignStyleType
    layoutInstructions: str
    exportReadyData: dict[str, Any]


class NewsPhotocardGenerateResponse(BaseModel):
    success: bool
    message: str
    data: NewsPhotocardData


class NewsPhotocardExportRequest(BaseModel):
    headline: str = Field(..., min_length=1, max_length=200)
    subheadline: str = Field(default="", max_length=300)
    category: str = Field(..., min_length=1, max_length=80)
    aspect_ratio: NewsAspectRatioType = "4:5"
    tone: NewsToneType = "breaking-news"
    design_style: NewsDesignStyleType = "dark-red"
    language: NewsLanguageType = "en"
    has_logo: bool = False
    has_image: bool = False


class NewsPhotocardExportResponse(BaseModel):
    success: bool
    message: str
    export_id: str
    manifest_url: str
    server_png_ready: bool = False
