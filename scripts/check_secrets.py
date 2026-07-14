"""Fail on common committed secret assignments while avoiding user-content output."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".jar", ".lock"}
EXCLUDED_NAMES = {"check_secrets.py"}
PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|access[_-]?token|private[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{16,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
)


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [ROOT / path for path in result.stdout.splitlines() if path]


def main() -> int:
    findings: list[str] = []
    for path in tracked_files():
        if (
            not path.is_file()
            or path.suffix.lower() in EXCLUDED_SUFFIXES
            or path.name in EXCLUDED_NAMES
        ):
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(content) for pattern in PATTERNS):
            findings.append(str(path.relative_to(ROOT)))

    if findings:
        print("Potential secrets detected in:", file=sys.stderr)
        for finding in findings:
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Secret scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
