"""Intent classifier — maps natural-language prompts to content generators."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.models.content_schemas import GenerationParametersModel, IntentAlternativeModel, IntentClassifyResponse
from app.services.content.categories import CATEGORY_SPECS, get_category_spec
from app.services.openai_service import OpenAIService

CONFIDENCE_MANUAL_THRESHOLD = 0.55

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "breaking-news-cards": ("breaking news", "breaking alert", "urgent news", "news flash", "just in"),
    "news-photocards": ("photocard", "news photocard", "editorial card", "newsroom"),
    "event-posters": ("poster", "debate", "competition", "concert", "summit", "meetup", "workshop poster", "event"),
    "presentations": ("pitch deck", "presentation", "slide deck", "slides", "powerpoint", "ppt", "deck"),
    "certificates": ("certificate", "certificates", "award", "participants", "completion", "diploma"),
    "instagram-posts": ("instagram post", "instagram", "ig post", "feed post"),
    "instagram-stories": ("instagram story", "ig story", "story"),
    "facebook-posts": ("facebook post", "fb post"),
    "facebook-covers": ("facebook cover", "page cover", "fb cover"),
    "youtube-thumbnails": ("youtube thumbnail", "thumbnail", "yt thumb"),
    "youtube-community-posts": ("youtube community", "community post"),
    "political-posters": ("political", "campaign poster", "election"),
    "educational-posters": ("educational poster", "classroom", "learning poster"),
    "id-cards": ("id card", "badge", "employee card"),
    "flyers": ("flyer", "leaflet", "handout"),
    "brochures": ("brochure", "tri-fold", "pamphlet"),
    "infographics": ("infographic", "data viz", "stats graphic"),
    "resume-builder": ("resume", "cv", "curriculum vitae"),
    "invitation-cards": ("invitation", "invite", "rsvp", "wedding invite"),
    "ad-creatives": ("ad creative", "advertisement", "display ad"),
    "product-promotions": ("product promo", "product launch", "sale promo"),
    "ngo-campaign-materials": ("ngo", "nonprofit", "awareness campaign", "charity"),
    "real-estate-templates": ("real estate", "property listing", "listing card"),
    "restaurant-marketing": ("restaurant", "menu promo", "food promo", "dish"),
    "podcast-covers": ("podcast cover", "podcast art", "show artwork"),
}

CATEGORY_CATALOG = "\n".join(f"- {s.id}: {s.name} — {s.system_hint}" for s in CATEGORY_SPECS.values())

INTENT_SYSTEM_PROMPT = f"""You classify user design requests into exactly one SlideGen AI category.
Valid category_id values:
{CATEGORY_CATALOG}

Return ONLY JSON:
{{
  "category_id": string,
  "confidence": number (0.0-1.0),
  "reasoning": string,
  "title": string | null,
  "refined_prompt": string,
  "quantity": number | null,
  "aspect_ratio": "1:1"|"4:5"|"16:9"|"9:16"|"A4"|null,
  "language": "en"|"es"|"fr"|"de"|"ar"|"hi"|"bn"|"pt",
  "alternatives": [{{"category_id": string, "confidence": number}}]
}}

Rules:
- "breaking news photocard" -> breaking-news-cards (not news-photocards if breaking/urgent)
- "news photocard" without breaking -> news-photocards
- "debate competition poster" -> event-posters
- "startup pitch deck" -> presentations
- "N certificates" -> certificates with quantity=N
- Prefer the most specific category. Max 3 alternatives."""


@dataclass
class _Score:
    category_id: str
    score: float
    hits: list[str]


class IntentClassifierService:
    def __init__(self) -> None:
        self._openai = OpenAIService()

    def classify(self, prompt: str) -> IntentClassifyResponse:
        prompt = prompt.strip()
        if len(prompt) < 3:
            return self._manual_fallback(prompt, "Prompt too short.")

        ai = self._classify_with_openai(prompt)
        if ai:
            return ai

        return self._classify_with_heuristics(prompt)

    def _classify_with_openai(self, prompt: str) -> IntentClassifyResponse | None:
        if not self._openai.enabled:
            return None
        raw = self._openai._chat_json(INTENT_SYSTEM_PROMPT, f"User request:\n{prompt}", max_tokens=1024)
        if not raw or not isinstance(raw.get("category_id"), str):
            return None

        category_id = str(raw["category_id"])
        if category_id not in CATEGORY_SPECS:
            category_id = "presentations"

        confidence = min(1.0, max(0.0, float(raw.get("confidence", 0.7))))
        spec = get_category_spec(category_id)
        params = self._build_parameters(prompt, raw, spec.default_aspect)

        alts: list[IntentAlternativeModel] = []
        for item in (raw.get("alternatives") or [])[:3]:
            if isinstance(item, dict) and item.get("category_id") in CATEGORY_SPECS:
                alt_spec = get_category_spec(str(item["category_id"]))
                alts.append(
                    IntentAlternativeModel(
                        category_id=alt_spec.id,
                        category_name=alt_spec.name,
                        confidence=min(1.0, max(0.0, float(item.get("confidence", 0.3)))),
                    )
                )

        return IntentClassifyResponse(
            success=True,
            category_id=spec.id,
            category_name=spec.name,
            confidence=confidence,
            reasoning=str(raw.get("reasoning", f"Matched {spec.name} from your description.")),
            requires_manual_selection=confidence < CONFIDENCE_MANUAL_THRESHOLD,
            parameters=params,
            alternatives=alts,
        )

    def _classify_with_heuristics(self, prompt: str) -> IntentClassifyResponse:
        lower = prompt.lower()
        scores: list[_Score] = []

        for cat_id, keywords in CATEGORY_KEYWORDS.items():
            hits = [kw for kw in keywords if kw in lower]
            if hits:
                scores.append(_Score(cat_id, len(hits) + max(len(h) for h in hits) * 0.05, hits))

        if "breaking" in lower and ("news" in lower or "photocard" in lower):
            scores.append(_Score("breaking-news-cards", 3.5, ["breaking news"]))
        if "photocard" in lower and "breaking" not in lower:
            scores.append(_Score("news-photocards", 2.5, ["photocard"]))
        if re.search(r"\b\d+\s+certificates?\b", lower):
            scores.append(_Score("certificates", 4.0, ["bulk certificates"]))
        if "pitch" in lower and "deck" in lower:
            scores.append(_Score("presentations", 3.5, ["pitch deck"]))
        if "poster" in lower and any(w in lower for w in ("debate", "competition", "tournament")):
            scores.append(_Score("event-posters", 3.0, ["event poster"]))

        scores.sort(key=lambda s: s.score, reverse=True)

        if not scores:
            return self._manual_fallback(prompt, "Could not confidently match a category.")

        best = scores[0]
        spec = get_category_spec(best.category_id)
        max_score = best.score
        confidence = min(0.92, 0.38 + max_score * 0.12)
        if len(scores) > 1 and scores[1].score >= best.score * 0.85:
            confidence *= 0.75

        alts = [
            IntentAlternativeModel(
                category_id=get_category_spec(s.category_id).id,
                category_name=get_category_spec(s.category_id).name,
                confidence=min(0.85, confidence * (0.9 - i * 0.15)),
            )
            for i, s in enumerate(scores[1:4])
        ]

        raw_params: dict = {"refined_prompt": prompt, "title": self._extract_title(prompt)}
        qty = self._extract_quantity(prompt)
        if qty:
            raw_params["quantity"] = qty

        return IntentClassifyResponse(
            success=True,
            category_id=spec.id,
            category_name=spec.name,
            confidence=round(confidence, 3),
            reasoning=f"Detected {spec.name} from keywords: {', '.join(best.hits[:3])}.",
            requires_manual_selection=confidence < CONFIDENCE_MANUAL_THRESHOLD,
            parameters=self._build_parameters(prompt, raw_params, spec.default_aspect),
            alternatives=alts,
        )

    def _manual_fallback(self, prompt: str, reasoning: str) -> IntentClassifyResponse:
        spec = get_category_spec("presentations")
        return IntentClassifyResponse(
            success=True,
            category_id=spec.id,
            category_name=spec.name,
            confidence=0.25,
            reasoning=reasoning,
            requires_manual_selection=True,
            parameters=self._build_parameters(prompt, {"refined_prompt": prompt}, spec.default_aspect),
            alternatives=[
                IntentAlternativeModel(category_id=c.id, category_name=c.name, confidence=0.2)
                for c in list(CATEGORY_SPECS.values())[:5]
            ],
        )

    def _build_parameters(self, prompt: str, raw: dict, default_aspect: str) -> GenerationParametersModel:
        aspect = raw.get("aspect_ratio")
        valid_aspects = {"1:1", "4:5", "16:9", "9:16", "A4"}
        aspect_ratio = aspect if aspect in valid_aspects else default_aspect

        lang = raw.get("language", "en")
        valid_langs = {"en", "es", "fr", "de", "ar", "hi", "bn", "pt"}
        language = lang if lang in valid_langs else "en"

        qty = raw.get("quantity")
        quantity = int(qty) if isinstance(qty, (int, float)) and qty > 0 else self._extract_quantity(prompt)

        title = raw.get("title")
        refined = str(raw.get("refined_prompt", prompt)).strip() or prompt

        return GenerationParametersModel(
            refined_prompt=refined,
            title=str(title) if title else self._extract_title(prompt),
            quantity=quantity,
            aspect_ratio=aspect_ratio,
            language=language,
        )

    def _extract_quantity(self, prompt: str) -> int | None:
        m = re.search(r"\b(\d{1,5})\s+certificates?\b", prompt, re.I)
        if m:
            return int(m.group(1))
        m = re.search(r"\bcreate\s+(\d{1,5})\b", prompt, re.I)
        if m and "certificate" in prompt.lower():
            return int(m.group(1))
        return None

    def _extract_title(self, prompt: str) -> str | None:
        cleaned = prompt.strip().rstrip(".")
        if len(cleaned) <= 80:
            return cleaned
        return cleaned[:77] + "..."
