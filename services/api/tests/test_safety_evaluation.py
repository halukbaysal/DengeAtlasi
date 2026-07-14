import json
from pathlib import Path
from typing import Any

from services.api.app.safety import SafetyOutcome, classify_safety

FIXTURE = Path(__file__).parent / "fixtures" / "sprint04" / "safety_eval.json"


def test_sprint04_safety_evaluation_fixture() -> None:
    cases: list[dict[str, Any]] = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for case in cases:
        outcome = classify_safety(str(case["query"])).outcome
        assert outcome == SafetyOutcome(str(case["expectedStatus"]))
