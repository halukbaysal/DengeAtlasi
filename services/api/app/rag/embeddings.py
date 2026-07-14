from __future__ import annotations

import re
from collections.abc import Sequence
from hashlib import sha256
from math import sqrt
from typing import Protocol


class EmbeddingProvider(Protocol):
    @property
    def provider_id(self) -> str: ...

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class DeterministicTestEmbeddingProvider:
    """Synthetic test-only embeddings; never a production model selection."""

    def __init__(self, dimensions: int = 16) -> None:
        if dimensions < 2:
            raise ValueError("dimensions must be at least 2")
        self._dimensions = dimensions

    @property
    def provider_id(self) -> str:
        return f"deterministic-test-v2-{self._dimensions}d"

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        output = [0.0] * self._dimensions
        tokens = re.findall(r"\w+", text.casefold(), flags=re.UNICODE)
        for token in tokens:
            digest = sha256(token.encode()).digest()
            index = int.from_bytes(digest[:4], "big") % self._dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            output[index] += sign
        magnitude = sqrt(sum(value * value for value in output))
        return [value / magnitude for value in output] if magnitude else output
