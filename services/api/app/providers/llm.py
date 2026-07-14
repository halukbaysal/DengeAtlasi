from collections.abc import Mapping
from typing import Any, Protocol


class ProviderTimeout(Exception):
    pass


class InvalidProviderResponse(Exception):
    pass


class LLMProvider(Protocol):
    def generate(self, context: Mapping[str, Any], *, timeout_seconds: float) -> Any:
        """Return structured data; callers must treat it as untrusted."""


class MockLLMProvider:
    def __init__(self, response: Any = None, *, error: Exception = None) -> None:  # type: ignore[assignment]
        self._response = response
        self._error = error

    def generate(self, context: Mapping[str, Any], *, timeout_seconds: float) -> Any:
        del context, timeout_seconds
        if self._error is not None:
            raise self._error
        return self._response
