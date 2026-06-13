import json
import os
from typing import Any

from openai import OpenAI
from pydantic import ValidationError

from app.models.schemas import NoteRequestSlide, SlideOutlineItem, SpeakerNoteItem
from app.services.ai_response import (
    normalize_analysis_payload,
    normalize_outline_payload,
    normalize_revision_outline,
    normalize_speaker_notes_payload,
    parse_json_object_from_content,
)
from app.services.openai_prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    NOTES_SYSTEM_PROMPT,
    OUTLINE_SYSTEM_PROMPT,
    REVISION_SYSTEM_PROMPT,
    build_analysis_user_prompt,
    build_notes_user_prompt,
    build_outline_user_prompt,
    build_revision_user_prompt,
)


class OpenAIService:
    """OpenAI Chat Completions with JSON parsing, normalization, and safe fallbacks."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def generate_analysis_payload(
        self,
        document_text: str,
        filename: str,
        *,
        word_count: int,
        max_outline_slides: int | None = None,
    ) -> dict[str, Any] | None:
        """Returns a dict suitable for DocumentAnalysis.model_validate, or None."""
        if not self.enabled:
            return None
        cap = max_outline_slides or int(os.getenv("OPENAI_ANALYSIS_MAX_SLIDES", "14"))
        cap = max(4, min(20, cap))
        max_chars = int(os.getenv("OPENAI_MAX_DOCUMENT_CHARS", "48000"))
        text = document_text if len(document_text) <= max_chars else document_text[:max_chars]

        user_prompt = build_analysis_user_prompt(text, filename, max_slides_hint=cap)
        raw = self._chat_json(ANALYSIS_SYSTEM_PROMPT, user_prompt, max_tokens=8192)
        if not raw:
            return None
        return normalize_analysis_payload(raw, filename=filename, word_count=word_count)

    def generate_outline(
        self,
        document_summary: str,
        persona: str,
        theme: str,
        prompt: str | None,
        max_slides: int,
    ) -> list[SlideOutlineItem] | None:
        if not self.enabled:
            return None
        max_summary = int(os.getenv("OPENAI_MAX_SUMMARY_CHARS", "12000"))
        summary = document_summary if len(document_summary) <= max_summary else document_summary[:max_summary]
        user_prompt = build_outline_user_prompt(summary, persona, theme, prompt, max_slides)
        raw = self._chat_json(OUTLINE_SYSTEM_PROMPT, user_prompt, max_tokens=4096)
        if not raw:
            return None
        normalized = normalize_outline_payload(raw, max_slides=max_slides)
        if not normalized:
            return None
        try:
            return [SlideOutlineItem.model_validate(item) for item in normalized]
        except ValidationError:
            return None

    def generate_notes(self, slides: list[NoteRequestSlide]) -> list[SpeakerNoteItem] | None:
        if not self.enabled:
            return None
        slides_json = json.dumps([slide.model_dump() for slide in slides], ensure_ascii=True)
        raw = self._chat_json(NOTES_SYSTEM_PROMPT, build_notes_user_prompt(slides_json), max_tokens=4096)
        if not raw:
            return None
        normalized = normalize_speaker_notes_payload(raw)
        if not normalized:
            return None
        try:
            return [SpeakerNoteItem.model_validate(item) for item in normalized]
        except ValidationError:
            return None

    def revise_outline(
        self,
        instruction: str,
        persona: str,
        theme: str,
        outline: list[SlideOutlineItem],
    ) -> list[SlideOutlineItem] | None:
        if not self.enabled:
            return None
        outline_json = json.dumps([item.model_dump() for item in outline], ensure_ascii=True)
        raw = self._chat_json(
            REVISION_SYSTEM_PROMPT,
            build_revision_user_prompt(instruction, persona, theme, outline_json),
            max_tokens=4096,
        )
        if not raw:
            return None
        normalized = normalize_revision_outline(raw, max_slides=min(20, max(len(outline) + 6, len(outline))))
        if not normalized:
            return None
        try:
            return [SlideOutlineItem.model_validate(item) for item in normalized]
        except ValidationError:
            return None

    def _chat_json(self, system_prompt: str, user_prompt: str, *, max_tokens: int) -> dict[str, Any] | None:
        content = self._chat_content(system_prompt, user_prompt, max_tokens=max_tokens)
        if not content:
            return None
        return parse_json_object_from_content(content)

    def _chat_content(self, system_prompt: str, user_prompt: str, *, max_tokens: int) -> str | None:
        try:
            assert self.client is not None
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.25,
                max_tokens=max_tokens,
            )
            return (response.choices[0].message.content or "").strip() or None
        except Exception:
            return None
