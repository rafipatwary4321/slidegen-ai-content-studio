"""
Deterministic analysis when no LLM is available: derive title, summary, topics,
outline, and notes from extracted document text (real content, not canned copy).
"""

from __future__ import annotations

import re
from typing import Iterable

from app.models.schemas import DocumentAnalysis, SlideOutlineItem, SpeakerNoteItem


def _split_paragraphs(text: str) -> list[str]:
    raw = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not raw:
        return []
    parts = [p.strip() for p in re.split(r"\n\s*\n+", raw) if p.strip()]
    if len(parts) >= 2:
        return parts
    # Single block: split on sentence boundaries into pseudo-paragraphs
    sentences = re.split(r"(?<=[.!?])\s+", raw)
    chunks: list[str] = []
    buf: list[str] = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        buf.append(s)
        if sum(len(x) for x in buf) >= 320:
            chunks.append(" ".join(buf))
            buf = []
    if buf:
        chunks.append(" ".join(buf))
    return chunks if chunks else [raw]


def _title_from_filename(filename: str) -> str:
    stem = (filename or "document").rsplit(".", 1)[0].strip()
    return stem.replace("_", " ").replace("-", " ")[:120] or "Presentation"


def build_document_derived_analysis(document_text: str, filename: str, word_count: int) -> DocumentAnalysis:
    paragraphs = _split_paragraphs(document_text)
    flat = " ".join(document_text.split())
    summary = (flat[:720] + "…") if len(flat) > 720 else flat

    first_line = ""
    if paragraphs:
        first_line = paragraphs[0].split("\n", 1)[0].strip()
    title = _title_from_filename(filename)
    if 4 <= len(first_line) <= 120:
        title = first_line[:120]

    key_topics: list[str] = []
    for p in paragraphs[:14]:
        head = p.split("\n", 1)[0].strip()
        if 24 <= len(head) <= 110 and head not in key_topics:
            key_topics.append(head[:100])
        if len(key_topics) >= 6:
            break
    if not key_topics:
        key_topics = ["Document structure", "Key messages", "Supporting detail", "Conclusions and next steps"]

    chart_suggestions = []
    if re.search(r"\b\d{1,3}(?:[.,]\d{3})*(?:\s*%|\s+percent)\b", document_text, re.I):
        chart_suggestions.append("Percentages detected — a bar or pie chart can highlight share or growth.")
    if re.search(r"\b20\d{2}\b|\bQ[1-4]\b", document_text):
        chart_suggestions.append("Dates or quarters mentioned — consider a timeline or trend chart.")
    if not chart_suggestions:
        chart_suggestions.append("Add a simple chart if you introduce metrics or comparisons later.")

    outline: list[SlideOutlineItem] = []
    max_slides = min(8, max(3, len(paragraphs)))
    for idx, para in enumerate(paragraphs[:max_slides], start=1):
        lines = [ln.strip() for ln in para.split("\n") if ln.strip()]
        slide_title = (lines[0][:140] if lines else para[:140]).strip() or f"Section {idx}"
        bullets: list[str] = []
        for ln in lines[1:6]:
            if len(bullets) >= 4:
                break
            if len(ln) >= 8:
                bullets.append(ln[:120])
        if not bullets:
            snippet = para.replace("\n", " ").strip()
            if len(snippet) > len(slide_title) + 20:
                rest = snippet[len(slide_title) :].strip()[:360]
                for piece in re.split(r"[.;]\s+", rest):
                    p2 = piece.strip()
                    if len(p2) >= 12 and len(bullets) < 4:
                        bullets.append(p2[:120])
        if not bullets:
            bullets = ["Key point drawn from this section of your document."]
        outline.append(SlideOutlineItem(slide_number=idx, title=slide_title[:140], bullets=bullets[:4]))

    if len(outline) < 3:
        outline = [
            SlideOutlineItem(slide_number=1, title=title, bullets=["Overview from your uploaded source."]),
            SlideOutlineItem(
                slide_number=2,
                title="Main themes",
                bullets=key_topics[:3] if key_topics else ["Theme one", "Theme two"],
            ),
            SlideOutlineItem(
                slide_number=3,
                title="Next steps",
                bullets=["Review generated outline", "Refine with prompts", "Export to PowerPoint"],
            ),
        ]

    notes: list[SpeakerNoteItem] = []
    for slide in outline:
        notes.append(
            SpeakerNoteItem(
                slide_number=slide.slide_number,
                note=(
                    f'Speaker focus for "{slide.title}": expand using the original document; '
                    "tie bullets to evidence or examples from the source."
                ),
            )
        )

    return DocumentAnalysis(
        filename=filename,
        document_type="general",
        persona="Business",
        recommended_theme=None,
        presentation_title=title,
        summary=summary or "Summary generated from your document text.",
        word_count=word_count,
        key_topics=key_topics[:10],
        chart_suggestions=chart_suggestions[:10],
        outline=outline,
        speaker_notes=notes,
        sentiment="neutral",
    )
