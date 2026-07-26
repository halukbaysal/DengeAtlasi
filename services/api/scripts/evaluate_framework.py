from __future__ import annotations

import argparse
from pathlib import Path

from services.api.app.evaluation.reporting import write_reports
from services.api.app.evaluation.runner import load_inputs, run_evaluation

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATASET = ROOT / "evaluation/datasets/framework_validation/cases.json"
DEFAULT_FIXTURES = ROOT / "evaluation/fixtures/framework_outputs.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Sprint 09.5A eval framework.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--output", type=Path, default=ROOT / "evaluation/reports")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dataset, fixtures = load_inputs(args.dataset, args.fixtures)
    if args.validate_only:
        print(f"Validated {len(dataset.cases)} framework cases: NOT_PRODUCTION_EVIDENCE")
        return 0
    if args.smoke:
        selected_ids: set[str] = set()
        seen_categories: set[str] = set()
        for case in dataset.cases:
            if case.category.value not in seen_categories or len(selected_ids) < 20:
                selected_ids.add(case.case_id)
                seen_categories.add(case.category.value)
            if len(selected_ids) >= 20 and len(seen_categories) == 12:
                break
        dataset = dataset.model_copy(
            update={"cases": [case for case in dataset.cases if case.case_id in selected_ids]}
        )
        fixtures = fixtures.model_copy(
            update={
                "outputs": [
                    output for output in fixtures.outputs if output.case_id in selected_ids
                ]
            }
        )
    run = run_evaluation(dataset, fixtures)
    json_path, markdown_path = write_reports(run, args.output)
    try:
        json_display = json_path.relative_to(ROOT)
        markdown_display = markdown_path.relative_to(ROOT)
    except ValueError:
        json_display = json_path
        markdown_display = markdown_path
    print(f"{run.case_count} cases — FRAMEWORK_VALIDATION_ONLY — NOT_PRODUCTION_EVIDENCE")
    print(f"JSON: {json_display}")
    print(f"Markdown: {markdown_display}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
