"""Mock news photocard generator — structured output for MVP preview and export."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.models.news_photocard_schemas import (
    NewsPhotocardAiCopyData,
    NewsPhotocardAiCopyRequest,
    NewsPhotocardAiCopyResponse,
    NewsPhotocardData,
    NewsPhotocardGenerateRequest,
    NewsPhotocardGenerateResponse,
)
from app.services.openai_service import OpenAIService

CATEGORY_LABELS = {
    "politics": "Politics",
    "campus": "Campus",
    "sports": "Sports",
    "international": "International",
    "business": "Business",
    "entertainment": "Entertainment",
}

TONE_META = {
    "breaking-news": {
        "label": "Breaking News",
        "layout": "Full-bleed hero image with urgent red alert strip, oversized headline, timestamp footer.",
        "headlineScale": 1.15,
        "badgeStyle": "alert",
    },
    "premium-editorial": {
        "label": "Premium Editorial",
        "layout": "Magazine grid with generous whitespace, serif headline, gold rule divider, refined subhead.",
        "headlineScale": 1.0,
        "badgeStyle": "editorial",
    },
    "youth-media": {
        "label": "Youth Media",
        "layout": "Bold sans headline, gradient accent bar, dynamic angle crop on hero image, punchy subhead.",
        "headlineScale": 1.08,
        "badgeStyle": "youth",
    },
    "corporate-press": {
        "label": "Corporate Press",
        "layout": "Clean corporate masthead, logo top-right, structured headline block, muted footer source line.",
        "headlineScale": 0.95,
        "badgeStyle": "corporate",
    },
}

STYLE_PALETTES = {
    "dark-red": {
        "background": "#140505",
        "surface": "#1f0a0a",
        "accent": "#b91c1c",
        "text": "#ffffff",
        "muted": "#fca5a5",
        "badge": "#dc2626",
        "gold": "#d4af37",
    },
    "black": {
        "background": "#0a0a0a",
        "surface": "#141414",
        "accent": "#ffffff",
        "text": "#f5f5f5",
        "muted": "#a3a3a3",
        "badge": "#262626",
        "gold": "#c9a227",
    },
    "white": {
        "background": "#f7f7f7",
        "surface": "#ffffff",
        "accent": "#111111",
        "text": "#111111",
        "muted": "#525252",
        "badge": "#e5e5e5",
        "gold": "#b8860b",
    },
    "gold": {
        "background": "#1c1408",
        "surface": "#2a1f0c",
        "accent": "#d4af37",
        "text": "#faf5e6",
        "muted": "#e8d5a8",
        "badge": "#92700c",
        "gold": "#ffd700",
    },
}

ASPECT_DIMS = {
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "9:16": (1080, 1920),
}

AI_COPY_SYSTEM = """You are a senior digital news editor crafting copy for social photocards.
Return ONLY valid JSON with this exact shape:
{
  "headline": string,
  "subheadline": string,
  "category": "politics" | "campus" | "sports" | "international" | "business" | "entertainment",
  "tone": "breaking-news" | "premium-editorial" | "youth-media" | "corporate-press",
  "layoutDirection": string
}
Rules:
- Headline: max 12 words, punchy, photocard-friendly, not clickbait.
- Subheadline: max 28 words, adds context.
- layoutDirection: one short sentence about visual emphasis.
- Match the requested output language exactly."""

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "sports": ("sport", "football", "cricket", "match", "league", "athlete", "ক্রিকেট", "খেলা"),
    "campus": ("campus", "university", "college", "student", "exam", "বিশ্ববিদ্যালয়", "ক্যাম্পাস"),
    "international": ("international", "global", "foreign", "world", "abroad", "আন্তর্জাতিক", "বিশ্ব"),
    "business": ("business", "economy", "market", "stock", "trade", "ব্যবসা", "অর্থনীতি"),
    "entertainment": ("entertainment", "film", "movie", "music", "celebrity", "বিনোদন", "সিনেমা"),
    "politics": ("politics", "government", "election", "minister", "parliament", "রাজনীতি", "সরকার"),
}


class NewsPhotocardService:
    def __init__(self) -> None:
        self._openai = OpenAIService()

    def generate_copy(self, request: NewsPhotocardAiCopyRequest) -> NewsPhotocardAiCopyResponse:
        prompt = request.prompt.strip()
        ai_result = self._openai_copy(prompt, request.language)
        if ai_result:
            data = self._normalize_ai_copy(ai_result, prompt, request.language, source="openai")
            return NewsPhotocardAiCopyResponse(
                success=True,
                message="AI copy generated.",
                data=data,
            )

        data = self._mock_copy(prompt, request.language)
        return NewsPhotocardAiCopyResponse(
            success=True,
            message="Copy generated with offline fallback.",
            data=data,
        )

    def generate(self, request: NewsPhotocardGenerateRequest) -> NewsPhotocardGenerateResponse:
        headline = request.headline.strip()
        if not headline and request.ai_prompt:
            copy = self.generate_copy(
                NewsPhotocardAiCopyRequest(prompt=request.ai_prompt.strip(), language=request.language)
            )
            headline = copy.data.headline
            request = request.model_copy(
                update={
                    "headline": headline,
                    "subheadline": request.subheadline.strip() or copy.data.subheadline,
                    "news_category": copy.data.category,
                    "tone": copy.data.tone,
                }
            )
        elif not headline:
            raise ValueError("Headline or AI prompt is required.")

        category_label = CATEGORY_LABELS[request.news_category]
        tone_meta = TONE_META[request.tone]
        palette = STYLE_PALETTES[request.design_style]
        w, h = ASPECT_DIMS[request.aspect_ratio]
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%d %b %Y")

        headline = request.headline.strip()
        subheadline = request.subheadline.strip() or self._default_subheadline(request)
        title = headline[:80]

        layout_instructions = (
            f"{tone_meta['layout']} "
            f"Category badge: {category_label}. "
            f"Palette: {request.design_style.replace('-', ' ')}. "
            f"Canvas {w}×{h} ({request.aspect_ratio}). "
            f"Language: {'Bengali' if request.language == 'bn' else 'English'}."
        )
        if request.ai_prompt:
            layout_instructions += f" Creative direction: {request.ai_prompt.strip()[:400]}"

        export_ready = {
            "projectId": str(uuid4()),
            "categoryId": "news-photocards",
            "canvas": {"width": w, "height": h, "aspectRatio": request.aspect_ratio},
            "palette": palette,
            "tone": request.tone,
            "toneLabel": tone_meta["label"],
            "newsCategory": request.news_category,
            "newsCategoryLabel": category_label,
            "language": request.language,
            "date": date_str,
            "typography": {
                "headlineFont": "Noto Sans Bengali" if request.language == "bn" else "Georgia",
                "bodyFont": "Noto Sans Bengali" if request.language == "bn" else "Inter",
                "headlineSize": int(56 * tone_meta["headlineScale"]),
                "subheadlineSize": 22,
            },
            "layers": self._build_layers(headline, subheadline, category_label, date_str, palette, w, h, request),
            "assets": {
                "hasLogo": request.has_logo,
                "hasHeroImage": request.has_image,
            },
            "recommendedExports": ["png", "jpg", "pdf"],
        }

        data = NewsPhotocardData(
            title=title,
            headline=headline,
            subheadline=subheadline,
            category=category_label,
            language=request.language,
            aspectRatio=request.aspect_ratio,
            tone=request.tone,
            designStyle=request.design_style,
            layoutInstructions=layout_instructions,
            exportReadyData=export_ready,
        )

        return NewsPhotocardGenerateResponse(
            success=True,
            message="News photocard design generated.",
            data=data,
        )

    def _default_subheadline(self, request: NewsPhotocardGenerateRequest) -> str:
        if request.language == "bn":
            return "বিস্তারিত রিপোর্ট শীঘ্রই আপডেট করা হবে।"
        return "Full coverage and analysis — stay tuned for updates."

    def _build_layers(
        self,
        headline: str,
        subheadline: str,
        category: str,
        date_str: str,
        palette: dict[str, str],
        w: int,
        h: int,
        request: NewsPhotocardGenerateRequest,
    ) -> list[dict]:
        return [
            {"type": "shape", "name": "Background", "fill": palette["background"], "x": 0, "y": 0, "width": w, "height": h},
            {"type": "shape", "name": "AccentBar", "fill": palette["accent"], "x": 0, "y": 0, "width": w, "height": int(h * 0.06)},
            {
                "type": "text",
                "name": "CategoryBadge",
                "content": category.upper(),
                "fill": palette["badge"],
                "x": int(w * 0.06),
                "y": int(h * 0.08),
                "width": int(w * 0.4),
                "height": 48,
            },
            {
                "type": "text",
                "name": "Headline",
                "content": headline,
                "fill": palette["text"],
                "x": int(w * 0.06),
                "y": int(h * 0.18),
                "width": int(w * 0.88),
                "height": int(h * 0.28),
            },
            {
                "type": "text",
                "name": "Subheadline",
                "content": subheadline,
                "fill": palette["muted"],
                "x": int(w * 0.06),
                "y": int(h * 0.5),
                "width": int(w * 0.88),
                "height": int(h * 0.15),
            },
            {
                "type": "image",
                "name": "HeroImage",
                "content": "hero-placeholder",
                "x": int(w * 0.06),
                "y": int(h * 0.66),
                "width": int(w * 0.88),
                "height": int(h * 0.22),
                "visible": request.has_image,
            },
            {
                "type": "image",
                "name": "Logo",
                "content": "logo-placeholder",
                "x": int(w * 0.78),
                "y": int(h * 0.08),
                "width": int(w * 0.14),
                "height": int(w * 0.14),
                "visible": request.has_logo,
            },
            {
                "type": "text",
                "name": "DateLine",
                "content": date_str,
                "fill": palette["gold"],
                "x": int(w * 0.06),
                "y": int(h * 0.92),
                "width": int(w * 0.5),
                "height": 36,
            },
        ]

    def _openai_copy(self, prompt: str, language: str) -> dict | None:
        if not self._openai.enabled:
            return None
        lang_label = "Bengali" if language == "bn" else "English"
        user = f"Output language: {lang_label}\nRough news brief:\n{prompt[:1500]}"
        return self._openai._chat_json(AI_COPY_SYSTEM, user, max_tokens=1024)

    def _normalize_ai_copy(self, raw: dict, prompt: str, language: str, *, source: str) -> NewsPhotocardAiCopyData:
        category = self._coerce_category(str(raw.get("category", "politics")))
        tone = self._coerce_tone(str(raw.get("tone", "breaking-news")))
        headline = self._trim_headline(str(raw.get("headline", "")).strip(), language)
        subheadline = self._trim_subheadline(str(raw.get("subheadline", "")).strip(), language)
        layout = str(raw.get("layoutDirection", "")).strip() or TONE_META[tone]["layout"]

        if not headline:
            return self._mock_copy(prompt, language)

        if not subheadline:
            subheadline = (
                "বিস্তারিত রিপোর্ট শীঘ্রই আপডেট করা হবে।"
                if language == "bn"
                else "Full coverage and analysis — stay tuned for updates."
            )

        return NewsPhotocardAiCopyData(
            headline=headline,
            subheadline=subheadline,
            category=category,  # type: ignore[arg-type]
            tone=tone,  # type: ignore[arg-type]
            layoutDirection=layout[:200],
            source=source,  # type: ignore[arg-type]
        )

    def _mock_copy(self, prompt: str, language: str) -> NewsPhotocardAiCopyData:
        category = self._detect_category(prompt)
        tone = self._detect_tone(prompt)
        headline, subheadline = self._mock_headlines(prompt, language, category, tone)
        return NewsPhotocardAiCopyData(
            headline=headline,
            subheadline=subheadline,
            category=category,
            tone=tone,
            layoutDirection=TONE_META[tone]["layout"][:200],
            source="mock",
        )

    def _detect_category(self, prompt: str) -> str:
        lower = prompt.lower()
        best = "politics"
        best_score = 0
        for cat_id, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in lower)
            if score > best_score:
                best_score = score
                best = cat_id
        return best

    def _detect_tone(self, prompt: str) -> str:
        lower = prompt.lower()
        urgent = ("breaking", "urgent", "alert", "just in", "জরুরি", "ব্রেকিং")
        youth = ("viral", "trending", "campus", "student", "যুব")
        corporate = ("company", "corporate", "press release", "কর্পোরেট")
        if any(k in lower for k in urgent):
            return "breaking-news"
        if any(k in lower for k in youth):
            return "youth-media"
        if any(k in lower for k in corporate):
            return "corporate-press"
        return "premium-editorial"

    def _mock_headlines(self, prompt: str, language: str, category: str, tone: str) -> tuple[str, str]:
        topic = prompt.strip().rstrip(".")
        if len(topic) > 80:
            topic = topic[:77] + "…"

        if language == "bn":
            prefix = "ব্রেকিং: " if tone == "breaking-news" else ""
            headline = self._trim_headline(f"{prefix}{topic}", language)
            subheadline = self._trim_subheadline(
                f"{CATEGORY_LABELS[category]} বিষয়ে বিস্তারিত রিপোর্ট ও বিশ্লেষণ শীঘ্রই আপডেট করা হবে।",
                language,
            )
            return headline, subheadline

        prefix = "Breaking: " if tone == "breaking-news" else ""
        headline = self._trim_headline(f"{prefix}{topic}", language)
        subheadline = self._trim_subheadline(
            f"{CATEGORY_LABELS[category]} coverage with context, reaction, and what happens next.",
            language,
        )
        return headline, subheadline

    def _coerce_category(self, value: str) -> str:
        normalized = value.lower().strip().replace(" ", "-")
        if normalized in CATEGORY_LABELS:
            return normalized
        for cat_id in CATEGORY_LABELS:
            if cat_id in normalized or CATEGORY_LABELS[cat_id].lower() in normalized:
                return cat_id
        return "politics"

    def _coerce_tone(self, value: str) -> str:
        normalized = value.lower().strip().replace(" ", "-").replace("_", "-")
        if normalized in TONE_META:
            return normalized
        return "breaking-news"

    def _trim_headline(self, text: str, language: str) -> str:
        if not text:
            return "Major development unfolds" if language == "en" else "বড় খবর আসছে"
        words = text.split()
        max_words = 12
        trimmed = " ".join(words[:max_words])
        return trimmed if len(trimmed) <= 120 else trimmed[:117] + "…"

    def _trim_subheadline(self, text: str, language: str) -> str:
        if not text:
            return (
                "বিস্তারিত রিপোর্ট শীঘ্রই আপডেট করা হবে।"
                if language == "bn"
                else "Full coverage and analysis — stay tuned for updates."
            )
        words = text.split()
        trimmed = " ".join(words[:28])
        return trimmed if len(trimmed) <= 200 else trimmed[:197] + "…"
