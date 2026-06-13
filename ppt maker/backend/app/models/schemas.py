from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field

PersonaType = Literal["Student", "Business", "Marketing", "Corporate"]
ThemeType = Literal["Cinematic Dark", "Professional Light"]

_ALLOWED_PERSONAS = frozenset({"Student", "Business", "Marketing", "Corporate"})
_ALLOWED_THEMES = frozenset({"Cinematic Dark", "Professional Light"})


def _coerce_persona(value: object) -> PersonaType:
    """Map free-form DB/LLM strings onto API literals (avoids response serialization crashes)."""
    s = str(value).strip() if value is not None else ""
    if s in _ALLOWED_PERSONAS:
        return s  # type: ignore[return-value]
    key = s.lower()
    for p in _ALLOWED_PERSONAS:
        if key == p.lower():
            return p  # type: ignore[return-value]
    return "Business"


def _coerce_theme(value: object) -> ThemeType:
    s = str(value).strip() if value is not None else ""
    if s in _ALLOWED_THEMES:
        return s  # type: ignore[return-value]
    low = s.lower()
    if "cinematic" in low or low.endswith("dark"):
        return "Cinematic Dark"
    if "professional" in low or low.endswith("light"):
        return "Professional Light"
    return "Professional Light"


CoercedPersona = Annotated[PersonaType, BeforeValidator(_coerce_persona)]
CoercedTheme = Annotated[ThemeType, BeforeValidator(_coerce_theme)]


class UploadedFileMeta(BaseModel):
    filename: str
    content_type: str
    extension: str
    size_bytes: int
    file_hash: str
    parser_status: str
    word_count: int
    character_count: int
    preview_snippet: str


class ParsedDocument(BaseModel):
    metadata: UploadedFileMeta
    extracted_text: str
    prepared_text: str


class UploadResponse(BaseModel):
    success: bool
    message: str
    upload: ParsedDocument


class AnalyzeDocumentRequest(BaseModel):
    filename: str = Field(..., examples=["input.pdf"])
    document_text: str = Field(..., min_length=1)


class DocumentAnalysis(BaseModel):
    filename: str
    document_type: str
    persona: CoercedPersona
    recommended_theme: CoercedTheme | None = Field(
        default=None,
        description="Model-suggested visual theme; optional for clients that ignore it.",
    )
    presentation_title: str
    summary: str
    word_count: int
    key_topics: list[str]
    chart_suggestions: list[str]
    outline: list["SlideOutlineItem"]
    speaker_notes: list["SpeakerNoteItem"]
    sentiment: str


class AnalyzeDocumentResponse(BaseModel):
    success: bool
    message: str
    parsed_document: ParsedDocument
    analysis: DocumentAnalysis


class GenerateOutlineRequest(BaseModel):
    document_summary: str = Field(..., min_length=1)
    persona: CoercedPersona = Field(default="Business")
    theme: CoercedTheme = Field(default="Professional Light")
    prompt: str | None = Field(default=None, max_length=500)
    max_slides: int = Field(default=6, ge=1, le=20)


class SlideOutlineItem(BaseModel):
    slide_number: int
    title: str = Field(..., min_length=1, max_length=140)
    bullets: list[str] = Field(default_factory=list, max_length=8)


class GenerateOutlineResponse(BaseModel):
    success: bool
    message: str
    outline: list[SlideOutlineItem]


class ReviseOutlineRequest(BaseModel):
    instruction: str = Field(..., min_length=2)
    persona: CoercedPersona = Field(default="Business")
    theme: CoercedTheme = Field(default="Professional Light")
    outline: list[SlideOutlineItem]
    presentation_id: str | None = None
    user_id: str | None = None


class ReviseOutlineResponse(BaseModel):
    success: bool
    message: str
    previous_outline: list[SlideOutlineItem]
    updated_outline: list[SlideOutlineItem]


class NoteRequestSlide(BaseModel):
    slide_number: int
    title: str
    bullets: list[str]


class GenerateNotesRequest(BaseModel):
    slides: list[NoteRequestSlide]


class SpeakerNoteItem(BaseModel):
    slide_number: int
    note: str


class GenerateNotesResponse(BaseModel):
    success: bool
    message: str
    notes: list[SpeakerNoteItem]


class ExportPptxRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    theme: CoercedTheme = Field(default="Professional Light")
    slides: list[SlideOutlineItem]
    speaker_notes: list[SpeakerNoteItem] = Field(default_factory=list)
    presentation_id: str | None = None
    user_id: str | None = None


class ExportResult(BaseModel):
    export_id: str
    title: str
    theme: str
    slide_count: int
    file_path: str
    download_url: str
    status: str


class ExportPptxResponse(BaseModel):
    success: bool
    message: str
    export: ExportResult


class SavePresentationRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    uploaded_filename: str = Field(..., min_length=1)
    persona: CoercedPersona
    theme: CoercedTheme
    outline: list[SlideOutlineItem]
    speaker_notes: list[SpeakerNoteItem]
    pptx_file_path: str | None = None
    user_id: str | None = None


class PresentationRecord(BaseModel):
    id: str
    title: str
    uploaded_filename: str
    user_id: str | None = None
    persona: CoercedPersona
    theme: CoercedTheme
    created_at: str
    outline: list[SlideOutlineItem]
    speaker_notes: list[SpeakerNoteItem]
    pptx_file_path: str | None = None


class SavePresentationResponse(BaseModel):
    success: bool
    message: str
    presentation: PresentationRecord


class ListPresentationsResponse(BaseModel):
    success: bool
    presentations: list[PresentationRecord]


class AuthUser(BaseModel):
    id: str
    email: str
    name: str | None = None


class SignUpRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=320)
    password: str = Field(..., min_length=6, max_length=128)
    name: str | None = Field(default=None, max_length=120)


class SignInRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=320)
    password: str = Field(..., min_length=6, max_length=128)


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: AuthUser
