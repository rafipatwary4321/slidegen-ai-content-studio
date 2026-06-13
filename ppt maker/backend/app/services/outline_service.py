from app.models.schemas import SlideOutlineItem
from app.services.openai_service import OpenAIService


class OutlineService:
    """Slide outline generation service with OpenAI + fallback."""

    def __init__(self) -> None:
        self.openai_service = OpenAIService()

    def generate_outline(
        self,
        document_summary: str,
        persona: str,
        theme: str,
        prompt: str | None,
        max_slides: int,
    ) -> list[SlideOutlineItem]:
        ai_outline = self.openai_service.generate_outline(
            document_summary=document_summary,
            persona=persona,
            theme=theme,
            prompt=prompt,
            max_slides=max_slides,
        )
        if ai_outline:
            return ai_outline

        base_titles = [
            "Title Slide",
            "Context and Opportunity",
            "Core Insights",
            "Proposed Approach",
            "Execution Plan",
            "Closing and Next Steps",
        ]

        chosen = base_titles[: max(1, min(max_slides, len(base_titles)))]

        return [
            SlideOutlineItem(
                slide_number=index + 1,
                title=title,
                bullets=[
                    "Main point 1",
                    "Main point 2",
                    "Main point 3",
                ],
            )
            for index, title in enumerate(chosen)
        ]

    def revise_outline(
        self,
        outline: list[SlideOutlineItem],
        instruction: str,
        persona: str,
        theme: str,
    ) -> list[SlideOutlineItem]:
        ai_revision = self.openai_service.revise_outline(
            instruction=instruction,
            persona=persona,
            theme=theme,
            outline=outline,
        )
        if ai_revision:
            return self._renumber(ai_revision)

        # Deterministic fallback when AI is unavailable/malformed.
        updated = [SlideOutlineItem.model_validate(item.model_dump()) for item in outline]
        lower = instruction.lower()
        if "shorten" in lower or "concise" in lower or "simplify" in lower:
            for slide in updated:
                slide.bullets = slide.bullets[:2]
                if "simplify" in lower:
                    slide.bullets = [f"Simple: {bullet}" for bullet in slide.bullets]
        if "professional" in lower or "investor" in lower:
            for slide in updated:
                slide.title = f"{slide.title} (Executive)"
        if "risk" in lower:
            updated.append(
                SlideOutlineItem(
                    slide_number=len(updated) + 1,
                    title="Risks and Mitigations",
                    bullets=[
                        "Key execution risks",
                        "Probability and impact assessment",
                        "Mitigation plan and owners",
                    ],
                )
            )
        if "student" in lower:
            for slide in updated:
                slide.bullets = [f"Student-friendly: {bullet}" for bullet in slide.bullets]

        return self._renumber(updated)

    @staticmethod
    def _renumber(outline: list[SlideOutlineItem]) -> list[SlideOutlineItem]:
        return [
            SlideOutlineItem(
                slide_number=index + 1,
                title=item.title,
                bullets=item.bullets,
            )
            for index, item in enumerate(outline)
        ]
