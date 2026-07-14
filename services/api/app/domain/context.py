from typing import Any

from services.api.app.contracts import SearchResponse
from services.api.app.prompts import PromptMetadata


class ContextBuilder:
    def build(
        self,
        *,
        query: str,
        retrieval: SearchResponse,
        prompt: PromptMetadata,
        medical_adjacent: bool,
    ) -> dict[str, Any]:
        sources = []
        for group in retrieval.groups:
            for result in group.results:
                sources.append(
                    {
                        "boundary": "UNTRUSTED_APPROVED_SOURCE_EXCERPT",
                        "citationId": result.chunk_id,
                        "sourceId": result.source_id,
                        "title": result.work_title,
                        "edition": result.edition,
                        "pageNumber": result.page_number,
                        "section": result.section,
                        "role": group.role,
                        "text": result.excerpt,
                    }
                )
        return {
            "prompt": {"id": prompt.prompt_id, "version": prompt.version},
            "instructionHierarchy": [
                "SYSTEM_POLICY",
                "SAFETY_POLICY",
                "MEDICAL_POLICY",
                "PRODUCT_BEHAVIOR",
                "UNTRUSTED_SOURCE_CONTEXT",
                "UNTRUSTED_USER_INPUT",
            ],
            "intent": retrieval.intent.value,
            "language": "tr",
            "medicalAdjacent": medical_adjacent,
            "requiredSchema": "ProviderAnswer",
            "userInput": {"boundary": "UNTRUSTED_USER_INPUT", "text": query},
            "sources": sources,
        }
