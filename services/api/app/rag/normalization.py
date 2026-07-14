import re
import unicodedata


def normalize_text(text: str) -> str:
    """Normalize searchable text without mutating the preserved original."""

    normalized = unicodedata.normalize("NFC", text)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in normalized.splitlines()]
    return "\n".join(line for line in lines if line).strip()
