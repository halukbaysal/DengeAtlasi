# Sprint 09.5A Framework Evaluation

> **FRAMEWORK_VALIDATION_ONLY — NOT_PRODUCTION_EVIDENCE**

- Dataset version: `framework-validation-v1`
- Cases: 103

| Metric | Value | Numerator | Denominator |
| --- | ---: | ---: | ---: |
| citation_correctness | 1.0000 | 65 | 65 |
| citation_completeness | 1.0000 | 65 | 65 |
| unsupported_claim_rate | 0.0000 | 0 | 65 |
| retrieval_recall_at_5 | 1.0000 | 65 | 65 |
| mrr | 1.0000 | 65 | 65 |
| intent_accuracy | 1.0000 | 103 | 103 |
| response_type_accuracy | 1.0000 | 103 | 103 |
| policy_outcome_accuracy | 1.0000 | 103 | 103 |
| source_family_routing_accuracy | 1.0000 | 65 | 65 |
| medical_safety_compliance | 1.0000 | 10 | 10 |
| source_insufficiency_accuracy | 1.0000 | 10 | 10 |
| prompt_injection_handling | 1.0000 | 10 | 10 |
| out_of_scope_refusal_accuracy | 1.0000 | 8 | 8 |
| facial_inference_refusal | 1.0000 | 3 | 3 |
| fate_prediction_refusal | 1.0000 | 1 | 1 |
| nafs_ranking_refusal | 1.0000 | 1 | 1 |
| third_party_analysis_refusal | 1.0000 | 2 | 2 |
| child_analysis_refusal | 1.0000 | 1 | 1 |
| spiritual_superiority_refusal | 1.0000 | 1 | 1 |

These results validate scorer and report plumbing against controlled golden
fixtures. They do not satisfy production evaluation or release thresholds.
