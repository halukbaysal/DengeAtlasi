from services.api.app.contracts import GeneratedClaim, RetrievalResult


class CitationValidationError(ValueError):
    pass


class CitationValidator:
    def validate(
        self, claims: list[GeneratedClaim], retrieved: list[RetrievalResult]
    ) -> list[RetrievalResult]:
        allowed = {item.chunk_id: item for item in retrieved}
        used: list[str] = []
        for claim in claims:
            cited_texts: list[str] = []
            for citation_id in claim.citation_ids:
                if citation_id not in allowed:
                    raise CitationValidationError("Provider returned an invented citation.")
                cited_texts.append(allowed[citation_id].excerpt)
                if citation_id not in used:
                    used.append(citation_id)
            claim_tokens = self._meaningful_tokens(claim.text)
            source_tokens = self._meaningful_tokens(" ".join(cited_texts))
            if not claim_tokens & source_tokens:
                raise CitationValidationError("Claim is not supported by its cited excerpt.")
        return [allowed[citation_id] for citation_id in used]

    @staticmethod
    def _meaningful_tokens(value: str) -> set[str]:
        return {
            token.strip(".,:;!?()[]{}\"'").casefold()
            for token in value.split()
            if len(token.strip(".,:;!?()[]{}\"'")) >= 4
        }
