from pathlib import Path

import pytest
from pydantic import ValidationError
from services.api.app.sources.governance import (
    GateDecision,
    HumanDecision,
    ProductionCollectionManifest,
    ProductionEditionRegistration,
    ProductionPageMetadata,
    UsageEnvironment,
)
from services.api.scripts.validate_production_knowledge import evaluate_registry


def pending_decision() -> HumanDecision:
    return HumanDecision()


def approved_decision(role: str) -> HumanDecision:
    return HumanDecision(
        status=GateDecision.APPROVED,
        reviewer=f"{role}-reviewer",
        decided_at="2026-07-26",
        evidence_reference=f"reviews/{role}.md",
    )


def registration(**overrides: object) -> ProductionEditionRegistration:
    values: dict[str, object] = {
        "source_id": "SRC-MAR-0001",
        "work_title": "Marifetname",
        "author": "Erzurumlu İbrahim Hakkı",
        "legal_review": pending_decision(),
        "ocr_review": pending_decision(),
        "content_review": pending_decision(),
        "final_approval": pending_decision(),
    }
    values.update(overrides)
    return ProductionEditionRegistration.model_validate(values)


def test_pending_registration_is_not_production_eligible() -> None:
    candidate = registration()
    assert not candidate.production_eligible
    assert "missing_edition" in candidate.blockers
    assert "legal_review_not_approved" in candidate.blockers


def test_all_independent_gates_are_required() -> None:
    candidate = registration(
        edition="Reviewed edition",
        publisher="Publisher",
        publication_year=2020,
        rights_holder="Rights holder",
        license_or_legal_basis="Written permission",
        usage_environment=UsageEnvironment.PRODUCTION,
        digital_provenance="Repository reference",
        page_number_confidence=1.0,
        ocr_suitability="Reviewed scan",
        legal_review=approved_decision("legal"),
        ocr_review=approved_decision("ocr"),
        content_review=approved_decision("content"),
        final_approval=approved_decision("final"),
    )
    assert candidate.production_eligible


def test_final_decision_cannot_omit_human_evidence() -> None:
    with pytest.raises(ValidationError):
        HumanDecision(status=GateDecision.APPROVED)


def test_page_metadata_requires_approved_status() -> None:
    with pytest.raises(ValidationError):
        ProductionPageMetadata(
            source_id="SRC-MAR-0001",
            author="Author",
            edition="Edition",
            publisher="Publisher",
            page=1,
            chapter="Chapter",
            topic="Topic",
            keywords=["keyword"],
            language="tr",
            source_family="Marifetname",
            review_status="UNREVIEWED",
        )


def test_collection_manifest_requires_restore_evidence() -> None:
    with pytest.raises(ValidationError):
        ProductionCollectionManifest(
            collection_name="denge_atlasi_prod_v1",
            source_count=1,
            page_count=1,
            chunk_count=1,
            source_hash="a" * 64,
            embedding_model="model",
            embedding_dimension=384,
            chunking_version="v1",
            created_at="2026-07-26T00:00:00Z",
            snapshot_reference="snapshot",
            backup_reference="backup",
        )


def test_current_registry_reports_blocked(tmp_path: Path) -> None:
    source = Path("data/reports/production-source-gate.json")
    target = tmp_path / "registry.json"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    report = evaluate_registry(target)
    assert report["status"] == "BLOCKED"
    assert report["production_evidence"] is False
    assert all(not item["production_eligible"] for item in report["registrations"])
