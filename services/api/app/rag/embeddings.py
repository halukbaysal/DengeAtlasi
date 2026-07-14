from __future__ import annotations

from collections.abc import Sequence
from hashlib import sha256
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
        return f"deterministic-test-v1-{self._dimensions}d"

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        output: list[float] = []
        counter = 0
        while len(output) < self._dimensions:
            digest = sha256(f"{counter}:{text}".encode()).digest()
            output.extend((byte / 127.5) - 1.0 for byte in digest)
            counter += 1
        return output[: self._dimensions]
