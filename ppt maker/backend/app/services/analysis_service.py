from pydantic import ValidationError

from app.models.schemas import DocumentAnalysis
from app.services.document_heuristics import build_document_derived_analysis
from app.services.openai_service import OpenAIService


class AnalysisService:
    """Document analysis: OpenAI structured JSON when configured, else document-derived heuristics."""

    def __init__(self) -> None:
        self.openai_service = OpenAIService()

    def analyze(self, document_text: str, filename: str) -> DocumentAnalysis:
        words = document_text.split()
        word_count = len(words)

        ai_payload = self.openai_service.generate_analysis_payload(
            document_text=document_text,
            filename=filename,
            word_count=word_count,
        )
        if ai_payload:
            try:
                return DocumentAnalysis.model_validate(ai_payload)
            except ValidationError:
                pass

        return build_document_derived_analysis(document_text, filename, word_count)
