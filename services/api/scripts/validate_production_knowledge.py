from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from services.api.app.sources.governance import ProductionEditionRegistration

DEFAULT_REGISTRY = Path("data/reports/production-source-gate.json")


def evaluate_registry(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    registrations = [
        ProductionEditionRegistration.model_validate(item)
        for item in payload["registrations"]
    ]
    sources = [
        {
            "source_id": registration.source_id,
            "production_eligible": registration.production_eligible,
            "blockers": registration.blockers,
        }
        for registration in registrations
    ]
    passed = bool(sources) and all(item["production_eligible"] for item in sources)
    return {
        "status": "PASS" if passed else "BLOCKED",
        "production_evidence": False,
        "registrations": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    report = evaluate_registry(args.registry)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and report["status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
