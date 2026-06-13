from app.models.schemas import NoteRequestSlide, SpeakerNoteItem
from app.services.openai_service import OpenAIService


class NotesService:
    """Speaker notes service with OpenAI + fallback."""

    def __init__(self) -> None:
        self.openai_service = OpenAIService()

    def generate_notes(self, slides: list[NoteRequestSlide]) -> list[SpeakerNoteItem]:
        ai_notes = self.openai_service.generate_notes(slides)
        if ai_notes:
            return ai_notes

        notes: list[SpeakerNoteItem] = []
        for slide in slides:
            note_text = (
                f"Speaker note for '{slide.title}'. Start with context, explain key bullet points, "
                "and close with a transition to the next slide."
            )
            notes.append(SpeakerNoteItem(slide_number=slide.slide_number, note=note_text))
        return notes
