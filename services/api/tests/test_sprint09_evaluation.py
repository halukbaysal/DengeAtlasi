from pathlib import Path

from services.api.scripts.evaluate_safety import evaluate


def test_sprint09_deterministic_safety_gates_pass() -> None:
    report = evaluate(Path("services/api/tests/fixtures/sprint09/security_eval.json"))
    assert report["passed"] is True
    assert all(item["passed"] for item in report["cases"])
