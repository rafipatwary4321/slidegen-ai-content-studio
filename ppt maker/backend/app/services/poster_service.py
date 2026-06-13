"""Poster generator — mock structured output for MVP preview and export."""

from __future__ import annotations

from uuid import uuid4

from app.models.poster_schemas import (
    PosterAiCopyData,
    PosterAiCopyRequest,
    PosterAiCopyResponse,
    PosterData,
    PosterGenerateRequest,
    PosterGenerateResponse,
)
from app.services.openai_service import OpenAIService

POSTER_TYPE_META = {
    "event": {"label": "Event Poster", "categoryId": "event-posters"},
    "political": {"label": "Political Poster", "categoryId": "political-posters"},
    "educational": {"label": "Educational Poster", "categoryId": "educational-posters"},
    "business": {"label": "Business Poster", "categoryId": "flyers"},
    "awareness": {"label": "Awareness Campaign", "categoryId": "ngo-campaign-materials"},
    "product": {"label": "Product Promotion", "categoryId": "product-promotions"},
}

TONE_META = {
    "premium-corporate": {
        "label": "Premium Corporate",
        "layout": "Centered hierarchy, navy accents, generous whitespace, refined CTA pill.",
        "palette": {"bg": "#0f172a", "surface": "#1e293b", "accent": "#38bdf8", "text": "#f8fafc", "muted": "#94a3b8", "cta": "#0ea5e9"},
    },
    "bold-political": {
        "label": "Bold Political",
        "layout": "High-contrast blocks, oversized title, strong divider, rally-style CTA bar.",
        "palette": {"bg": "#1a0505", "surface": "#2d0a0a", "accent": "#dc2626", "text": "#ffffff", "muted": "#fca5a5", "cta": "#b91c1c"},
    },
    "modern-youth": {
        "label": "Modern Youth",
        "layout": "Gradient header, dynamic image crop, playful typography, rounded CTA.",
        "palette": {"bg": "#1e1033", "surface": "#2d1b4e", "accent": "#a855f7", "text": "#faf5ff", "muted": "#d8b4fe", "cta": "#ec4899"},
    },
    "academic-clean": {
        "label": "Academic Clean",
        "layout": "Structured grid, clear sections for date/venue, minimal ornament, readable body.",
        "palette": {"bg": "#f8fafc", "surface": "#ffffff", "accent": "#1d4ed8", "text": "#0f172a", "muted": "#475569", "cta": "#2563eb"},
    },
    "luxury-event": {
        "label": "Luxury Event",
        "layout": "Gold accents, elegant serif title, spotlight hero image, premium footer band.",
        "palette": {"bg": "#1c1408", "surface": "#2a1f0c", "accent": "#d4af37", "text": "#faf5e6", "muted": "#e8d5a8", "cta": "#b8860b"},
    },
}

ASPECT_DIMS = {
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "9:16": (1080, 1920),
    "A4": (2480, 3508),
}

AI_COPY_SYSTEM = """You are a senior poster copywriter for print and social marketing.
Return ONLY valid JSON with this exact shape:
{
  "title": string,
  "subtitle": string,
  "ctaText": string,
  "posterType": "event" | "political" | "educational" | "business" | "awareness" | "product",
  "designTone": "premium-corporate" | "bold-political" | "modern-youth" | "academic-clean" | "luxury-event",
  "layoutDirection": string
}
Rules:
- title: max 10 words, bold and poster-friendly.
- subtitle: max 22 words, supportive context.
- ctaText: max 4 words, action-oriented (e.g. Register Now, Join Us).
- layoutDirection: one short sentence about visual emphasis.
- Match the requested output language exactly."""

TYPE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "political": ("election", "campaign", "vote", "minister", "rally", "নির্বাচন", "রাজনীতি"),
    "educational": ("school", "university", "campus", "exam", "workshop", "শিক্ষা", "ক্যাম্পাস"),
    "business": ("business", "corporate", "company", "startup", "ব্যবসা"),
    "awareness": ("awareness", "charity", "ngo", "donate", "সচেতনতা"),
    "product": ("product", "launch", "sale", "discount", "পণ্য"),
    "event": ("event", "concert", "summit", "conference", "festival", "ইভেন্ট"),
}

TONE_BY_TYPE: dict[str, str] = {
    "political": "bold-political",
    "educational": "academic-clean",
    "business": "premium-corporate",
    "awareness": "modern-youth",
    "product": "premium-corporate",
    "event": "luxury-event",
}


class PosterService:
    def __init__(self) -> None:
        self._openai = OpenAIService()

    def generate_copy(self, request: PosterAiCopyRequest) -> PosterAiCopyResponse:
        prompt = request.prompt.strip()
        ai_result = self._openai_copy(prompt, request.language)
        if ai_result:
            data = self._normalize_ai_copy(ai_result, prompt, request.language, source="openai")
            return PosterAiCopyResponse(success=True, message="AI copy generated.", data=data)
        data = self._mock_copy(prompt, request.language)
        return PosterAiCopyResponse(success=True, message="Copy generated with offline fallback.", data=data)

    def generate(self, request: PosterGenerateRequest) -> PosterGenerateResponse:
        title = request.title.strip()
        if not title and request.ai_prompt:
            copy = self.generate_copy(PosterAiCopyRequest(prompt=request.ai_prompt.strip(), language=request.language))
            title = copy.data.title
            request = request.model_copy(
                update={
                    "title": title,
                    "subtitle": request.subtitle.strip() or copy.data.subtitle,
                    "cta_text": copy.data.ctaText,
                    "poster_type": copy.data.posterType,
                    "design_tone": copy.data.designTone,
                }
            )
        elif not title:
            raise ValueError("Poster title or AI prompt is required.")

        title = request.title.strip() or self._default_title(request)
        subtitle = request.subtitle.strip() or self._default_subtitle(request)
        type_meta = POSTER_TYPE_META[request.poster_type]
        tone_meta = TONE_META[request.design_tone]
        palette = tone_meta["palette"]
        w, h = ASPECT_DIMS[request.aspect_ratio]

        layout_instructions = (
            f"{tone_meta['layout']} "
            f"Poster type: {type_meta['label']}. "
            f"Canvas {w}×{h} ({request.aspect_ratio}). "
            f"Language: {'Bengali' if request.language == 'bn' else 'English'}."
        )
        if request.date_time:
            layout_instructions += f" Feature date/time: {request.date_time}."
        if request.venue:
            layout_instructions += f" Venue block: {request.venue}."
        if request.ai_prompt:
            layout_instructions += f" Creative direction: {request.ai_prompt.strip()[:400]}"

        export_ready = {
            "projectId": str(uuid4()),
            "categoryId": type_meta["categoryId"],
            "posterType": request.poster_type,
            "posterTypeLabel": type_meta["label"],
            "canvas": {"width": w, "height": h, "aspectRatio": request.aspect_ratio},
            "palette": palette,
            "designTone": request.design_tone,
            "designToneLabel": tone_meta["label"],
            "language": request.language,
            "fields": {
                "title": title,
                "subtitle": subtitle,
                "dateTime": request.date_time,
                "venue": request.venue,
                "organizer": request.organizer,
                "ctaText": request.cta_text,
            },
            "layers": self._build_layers(request, title, subtitle, type_meta["label"], palette, w, h),
            "assets": {"hasLogo": request.has_logo, "hasHeroImage": request.has_image},
            "recommendedExports": ["png", "pdf", "jpg"],
        }

        data = PosterData(
            title=title,
            subtitle=subtitle,
            posterType=request.poster_type,
            language=request.language,
            aspectRatio=request.aspect_ratio,
            designTone=request.design_tone,
            layoutInstructions=layout_instructions,
            exportReadyData=export_ready,
        )

        return PosterGenerateResponse(success=True, message="Poster design generated.", data=data)

    def _default_title(self, request: PosterGenerateRequest) -> str:
        if request.language == "bn":
            return "আপনার ইভেন্টের শিরোনাম"
        return POSTER_TYPE_META[request.poster_type]["label"]

    def _default_subtitle(self, request: PosterGenerateRequest) -> str:
        if request.language == "bn":
            return "একটি শক্তিশালী উপশিরোনাম যোগ করুন"
        return "Add a compelling subtitle for your audience"

    def _build_layers(
        self,
        request: PosterGenerateRequest,
        title: str,
        subtitle: str,
        type_label: str,
        palette: dict[str, str],
        w: int,
        h: int,
    ) -> list[dict]:
        return [
            {"type": "shape", "name": "Background", "fill": palette["bg"], "x": 0, "y": 0, "width": w, "height": h},
            {"type": "text", "name": "TypeBadge", "content": type_label.upper(), "x": int(w * 0.08), "y": int(h * 0.06), "width": int(w * 0.5), "height": 40},
            {"type": "text", "name": "Title", "content": title, "x": int(w * 0.08), "y": int(h * 0.14), "width": int(w * 0.84), "height": int(h * 0.18)},
            {"type": "text", "name": "Subtitle", "content": subtitle, "x": int(w * 0.08), "y": int(h * 0.34), "width": int(w * 0.84), "height": int(h * 0.1)},
            {"type": "image", "name": "HeroImage", "visible": request.has_image, "x": int(w * 0.08), "y": int(h * 0.46), "width": int(w * 0.84), "height": int(h * 0.22)},
            {"type": "text", "name": "DateTime", "content": request.date_time or "", "x": int(w * 0.08), "y": int(h * 0.72), "width": int(w * 0.84), "height": 48},
            {"type": "text", "name": "Venue", "content": request.venue or "", "x": int(w * 0.08), "y": int(h * 0.76), "width": int(w * 0.84), "height": 48},
            {"type": "text", "name": "Organizer", "content": request.organizer or "", "x": int(w * 0.08), "y": int(h * 0.8), "width": int(w * 0.84), "height": 40},
            {"type": "shape", "name": "CtaButton", "fill": palette["cta"], "x": int(w * 0.08), "y": int(h * 0.86), "width": int(w * 0.4), "height": 56},
            {"type": "text", "name": "CtaText", "content": request.cta_text, "x": int(w * 0.1), "y": int(h * 0.865), "width": int(w * 0.36), "height": 48},
            {"type": "image", "name": "Logo", "visible": request.has_logo, "x": int(w * 0.78), "y": int(h * 0.06), "width": int(w * 0.12), "height": int(w * 0.12)},
        ]

    def _openai_copy(self, prompt: str, language: str) -> dict | None:
        if not self._openai.enabled:
            return None
        lang_label = "Bengali" if language == "bn" else "English"
        user = f"Output language: {lang_label}\nRough poster brief:\n{prompt[:1500]}"
        return self._openai._chat_json(AI_COPY_SYSTEM, user, max_tokens=1024)

    def _normalize_ai_copy(self, raw: dict, prompt: str, language: str, *, source: str) -> PosterAiCopyData:
        poster_type = self._coerce_type(str(raw.get("posterType", "event")))
        design_tone = self._coerce_tone(str(raw.get("designTone", TONE_BY_TYPE[poster_type])))
        title = self._trim_title(str(raw.get("title", "")).strip(), language)
        subtitle = self._trim_subtitle(str(raw.get("subtitle", "")).strip(), language)
        cta = self._trim_cta(str(raw.get("ctaText", "")).strip(), language)
        layout = str(raw.get("layoutDirection", "")).strip() or TONE_META[design_tone]["layout"]

        if not title:
            return self._mock_copy(prompt, language)

        if not subtitle:
            subtitle = self._default_subtitle_for_language(language)
        if not cta:
            cta = "এখনই যোগ দিন" if language == "bn" else "Register Now"

        return PosterAiCopyData(
            title=title,
            subtitle=subtitle,
            ctaText=cta,
            posterType=poster_type,  # type: ignore[arg-type]
            designTone=design_tone,  # type: ignore[arg-type]
            layoutDirection=layout[:200],
            source=source,  # type: ignore[arg-type]
        )

    def _mock_copy(self, prompt: str, language: str) -> PosterAiCopyData:
        poster_type = self._detect_type(prompt)
        design_tone = TONE_BY_TYPE[poster_type]
        title, subtitle, cta = self._mock_text(prompt, language, poster_type)
        return PosterAiCopyData(
            title=title,
            subtitle=subtitle,
            ctaText=cta,
            posterType=poster_type,  # type: ignore[arg-type]
            designTone=design_tone,  # type: ignore[arg-type]
            layoutDirection=TONE_META[design_tone]["layout"][:200],
            source="mock",
        )

    def _detect_type(self, prompt: str) -> str:
        lower = prompt.lower()
        best = "event"
        best_score = 0
        for type_id, keywords in TYPE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in lower)
            if score > best_score:
                best_score = score
                best = type_id
        return best

    def _mock_text(self, prompt: str, language: str, poster_type: str) -> tuple[str, str, str]:
        topic = prompt.strip().rstrip(".")
        if len(topic) > 70:
            topic = topic[:67] + "…"
        label = POSTER_TYPE_META[poster_type]["label"]

        if language == "bn":
            title = self._trim_title(topic or f"{label}", language)
            subtitle = self._trim_subtitle(f"{label} — আপনার অডিয়েন্সের জন্য শক্তিশালী বার্তা।", language)
            cta = "এখনই যোগ দিন"
            return title, subtitle, cta

        title = self._trim_title(topic or label, language)
        subtitle = self._trim_subtitle(f"{label} — compelling message crafted for maximum impact.", language)
        cta = "Register Now" if poster_type == "event" else "Learn More"
        return title, subtitle, cta

    def _coerce_type(self, value: str) -> str:
        normalized = value.lower().strip().replace(" ", "-")
        if normalized in POSTER_TYPE_META:
            return normalized
        for type_id, meta in POSTER_TYPE_META.items():
            if type_id in normalized or meta["label"].lower() in normalized:
                return type_id
        return "event"

    def _coerce_tone(self, value: str) -> str:
        normalized = value.lower().strip().replace(" ", "-").replace("_", "-")
        if normalized in TONE_META:
            return normalized
        return "luxury-event"

    def _trim_title(self, text: str, language: str) -> str:
        if not text:
            return "Your Poster Title" if language == "en" else "আপনার পোস্টার"
        words = text.split()
        trimmed = " ".join(words[:10])
        return trimmed if len(trimmed) <= 100 else trimmed[:97] + "…"

    def _trim_subtitle(self, text: str, language: str) -> str:
        if not text:
            return self._default_subtitle_for_language(language)
        words = text.split()
        trimmed = " ".join(words[:22])
        return trimmed if len(trimmed) <= 180 else trimmed[:177] + "…"

    def _trim_cta(self, text: str, language: str) -> str:
        if not text:
            return "এখনই যোগ দিন" if language == "bn" else "Learn More"
        words = text.split()
        return " ".join(words[:4])

    def _default_subtitle_for_language(self, language: str) -> str:
        if language == "bn":
            return "একটি শক্তিশালী উপশিরোনাম যোগ করুন"
        return "Add a compelling subtitle for your audience"
