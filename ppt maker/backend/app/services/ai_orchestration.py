"""
AI orchestration: single facade for analyze → outline → notes → revision.

Routes and higher-level services call this module to keep OpenAI wiring in one place.
"""

from __future__ import annotations

from app.models.schemas import (
    DocumentAnalysis,
    GenerateOutlineRequest,
    NoteRequestSlide,
    ReviseOutlineRequest,
    SlideOutlineItem,
    SpeakerNoteItem,
)
from app.services.analysis_service import AnalysisService
from app.services.notes_service import NotesService
from app.services.outline_service import OutlineService


class AIOrchestrationService:
    def __init__(self) -> None:
        self._analysis = AnalysisService()
        self._outline = OutlineService()
        self._notes = NotesService()

    def analyze_document(self, document_text: str, filename: str) -> DocumentAnalysis:
        return self._analysis.analyze(document_text, filename)

    def generate_outline(self, request: GenerateOutlineRequest) -> list[SlideOutlineItem]:
        return self._outline.generate_outline(
            document_summary=request.document_summary,
            persona=request.persona,
            theme=request.theme,
            prompt=request.prompt,
            max_slides=request.max_slides,
        )

    def revise_outline(self, request: ReviseOutlineRequest) -> list[SlideOutlineItem]:
        return self._outline.revise_outline(
            outline=request.outline,
            instruction=request.instruction,
            persona=request.persona,
            theme=request.theme,
        )

    def generate_speaker_notes(self, slides: list[NoteRequestSlide]) -> list[SpeakerNoteItem]:
        return self._notes.generate_notes(slides)
