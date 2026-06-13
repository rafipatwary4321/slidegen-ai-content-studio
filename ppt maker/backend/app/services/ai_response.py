"""
Parse and normalize OpenAI JSON outputs into API-safe structures for presentation generation.
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.models.schemas import _coerce_persona, _coerce_theme

_MAX_TITLE = 140
_MAX_BULLET = 140
_MAX_SLIDES = 20
_MAX_BULLETS_PER_SLIDE = 5
_MAX_SUMMARY = 2000
_MAX_NOTE = 1200


def parse_json_object_from_content(content: str) -> dict[str, Any] | None:
    """Extract a JSON object from model output (handles markdown fences and stray text)."""
    if not content or not content.strip():
        return None
    text = content.strip()
    # Strip ```json ... ``` or ``` ... ```
    fence = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", text, re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        pass
    # Last resort: first balanced-ish object (greedy inner braces avoided — take substring from first { to last })
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            data = json.loads(text[start : end + 1])
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def _trim(s: str, max_len: int) -> str:
    s = str(s).strip()
    return s[:max_len] if len(s) > max_len else s


def _normalize_string_list(value: Any, *, limit: int, item_max: int) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value[:limit]:
        if item is None:
            continue
        t = _trim(str(item), item_max)
        if t:
            out.append(t)
    return out


def normalize_analysis_payload(raw: dict[str, Any], *, filename: str, word_count: int) -> dict[str, Any] | None:
    """
    Turn a loose model JSON dict into fields compatible with DocumentAnalysis.model_validate.
    Returns None if outline cannot be salvaged.
    """
    outline_raw = raw.get("outline")
    if not isinstance(outline_raw, list) or not outline_raw:
        return None

    outline: list[dict[str, Any]] = []
    for idx, item in enumerate(outline_raw[:_MAX_SLIDES], start=1):
        if not isinstance(item, dict):
            continue
        title = _trim(str(item.get("title", f"Slide {idx}")), _MAX_TITLE) or f"Slide {idx}"
        bullets_in = item.get("bullets")
        bullets: list[str] = []
        if isinstance(bullets_in, list):
            for b in bullets_in[:_MAX_BULLETS_PER_SLIDE]:
                bt = _trim(str(b), _MAX_BULLET)
                if bt:
                    bullets.append(bt)
        if not bullets:
            bullets = ["Key takeaway from this section of the source document."]
        outline.append({"slide_number": idx, "title": title, "bullets": bullets})

    if not outline:
        return None

    slide_numbers = [o["slide_number"] for o in outline]
    notes_by_slide: dict[int, str] = {}
    sn_raw = raw.get("speaker_notes")
    if isinstance(sn_raw, list):
        for n in sn_raw:
            if not isinstance(n, dict):
                continue
            try:
                sn = int(n.get("slide_number"))
            except (TypeError, ValueError):
                continue
            note = _trim(str(n.get("note", "")), _MAX_NOTE)
            if sn in slide_numbers and note:
                notes_by_slide[sn] = note

    speaker_notes: list[dict[str, Any]] = []
    for o in outline:
        sn = int(o["slide_number"])
        title = o["title"]
        note = notes_by_slide.get(sn)
        if not note:
            note = (
                f'Present "{title}": walk through the bullets, tie each to evidence from the document, '
                "and transition clearly to the next slide."
            )
        speaker_notes.append({"slide_number": sn, "note": _trim(note, _MAX_NOTE)})

    persona = _coerce_persona(raw.get("persona", "Business"))
    rec_theme_raw = raw.get("recommended_theme")
    recommended_theme: str | None = None
    if rec_theme_raw is not None and str(rec_theme_raw).strip():
        recommended_theme = _coerce_theme(rec_theme_raw)

    return {
        "filename": filename,
        "document_type": _trim(str(raw.get("document_type", "general")), 80),
        "persona": persona,
        "recommended_theme": recommended_theme,
        "presentation_title": _trim(str(raw.get("presentation_title", filename)), 200),
        "summary": _trim(str(raw.get("summary", "")), _MAX_SUMMARY) or "Summary generated from the document.",
        "word_count": word_count,
        "key_topics": _normalize_string_list(raw.get("key_topics"), limit=10, item_max=120),
        "chart_suggestions": _normalize_string_list(raw.get("chart_suggestions"), limit=10, item_max=200),
        "outline": outline,
        "speaker_notes": speaker_notes,
        "sentiment": _trim(str(raw.get("sentiment", "neutral")), 20),
    }


def normalize_outline_payload(raw: dict[str, Any], *, max_slides: int) -> list[dict[str, Any]] | None:
    items = raw.get("outline")
    if not isinstance(items, list) or not items:
        return None
    cap = max(1, min(max_slides, _MAX_SLIDES))
    outline: list[dict[str, Any]] = []
    for idx, item in enumerate(items[:cap], start=1):
        if not isinstance(item, dict):
            continue
        title = _trim(str(item.get("title", f"Slide {idx}")), _MAX_TITLE) or f"Slide {idx}"
        bullets_in = item.get("bullets")
        bullets: list[str] = []
        if isinstance(bullets_in, list):
            for b in bullets_in[:_MAX_BULLETS_PER_SLIDE]:
                bt = _trim(str(b), _MAX_BULLET)
                if bt:
                    bullets.append(bt)
        if not bullets:
            bullets = ["Main point derived from the document summary."]
        outline.append({"slide_number": idx, "title": title, "bullets": bullets})
    return outline or None


def normalize_revision_outline(raw: dict[str, Any], *, max_slides: int) -> list[dict[str, Any]] | None:
    items = raw.get("updated_outline")
    if not isinstance(items, list) or not items:
        return None
    return normalize_outline_payload({"outline": items}, max_slides=max_slides)


def normalize_speaker_notes_payload(raw: dict[str, Any]) -> list[dict[str, Any]] | None:
    items = raw.get("speaker_notes")
    if not isinstance(items, list) or not items:
        return None
    out: list[dict[str, Any]] = []
    for n in items:
        if not isinstance(n, dict):
            continue
        try:
            sn = int(n.get("slide_number"))
        except (TypeError, ValueError):
            continue
        note = _trim(str(n.get("note", "")), _MAX_NOTE)
        if note:
            out.append({"slide_number": sn, "note": note})
    return out or None
