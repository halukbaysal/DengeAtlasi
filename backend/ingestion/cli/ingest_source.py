from __future__ import annotations

import argparse
from pathlib import Path

from backend.ingestion.registry import SourceRegistry


def _pdfs(path: Path | None, folder: Path | None) -> list[Path]:
    if path:
        return [path]
    if folder:
        return sorted(folder.glob("*.pdf"))
    raise ValueError("provide a PDF path or --folder")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="KS-01 immutable PDF registration; no OCR or classification"
    )
    parser.add_argument("path", type=Path, nargs="?")
    parser.add_argument("--folder", type=Path)
    parser.add_argument(
        "--library",
        type=Path,
        default=Path("data/source-library"),
        help="Local source-library root",
    )
    args = parser.parse_args()
    registry = SourceRegistry(args.library)
    paths = _pdfs(args.path, args.folder)
    if not paths:
        print("No PDF files found.")
        return 1
    for source in paths:
        result = registry.register_file(source)
        print(
            f"{source}: {result.record.source_id} / REGISTERED / UNTRUSTED / "
            f"duplicate={str(result.exact_duplicate).lower()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
