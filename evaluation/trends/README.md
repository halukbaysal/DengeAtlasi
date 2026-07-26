# Evaluation Trend Format

Each retained run is a JSON object with `evidence_label`, `dataset_version`,
`case_count`, and a metrics map containing `value`, `numerator`, and `denominator`.
Production and framework histories must never be merged. Generated history is not
committed until retention and review ownership are approved.
