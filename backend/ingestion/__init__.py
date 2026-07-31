"""Knowledge Studio source intake.

Legacy OCR/chunk/embedding prototype modules are deprecated and are not called by KS-01.
"""

from backend.ingestion.registry import SourceRegistry

__all__ = ["SourceRegistry"]
