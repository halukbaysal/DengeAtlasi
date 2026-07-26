from __future__ import annotations

import json
from pathlib import Path

from .runner import EvaluationRun


def write_reports(run: EvaluationRun, output_directory: Path) -> tuple[Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    json_path = output_directory / "framework-evaluation.json"
    markdown_path = output_directory / "framework-evaluation.md"
    json_path.write_text(
        json.dumps(run.as_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    rows = [
        "# Sprint 09.5A Framework Evaluation",
        "",
        "> **FRAMEWORK_VALIDATION_ONLY — NOT_PRODUCTION_EVIDENCE**",
        "",
        f"- Dataset version: `{run.dataset_version}`",
        f"- Cases: {run.case_count}",
        "",
        "| Metric | Value | Numerator | Denominator |",
        "| --- | ---: | ---: | ---: |",
    ]
    rows.extend(
        f"| {metric.name} | {metric.value:.4f} | {metric.numerator:g} | {metric.denominator} |"
        for metric in run.metrics
    )
    rows.extend(
        [
            "",
            "These results validate scorer and report plumbing against controlled golden",
            "fixtures. They do not satisfy production evaluation or release thresholds.",
        ]
    )
    markdown_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return json_path, markdown_path
