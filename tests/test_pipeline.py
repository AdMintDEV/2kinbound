from pathlib import Path

from forge.pipeline import Pipeline
from forge.storage import Store


def test_pipeline_scores_and_stores(tmp_path: Path) -> None:
    pipeline = Pipeline(Store(tmp_path / "forge.db"))
    result = pipeline.run_payload(
        [
            {
                "id": "full",
                "title": "Full record",
                "market": {"tam_usd": 500_000_000, "growth_rate": 0.2},
                "traction": {"users": 2000, "revenue_usd": 80000, "growth_rate": 0.15},
                "competition": {"intensity": 0.4, "incumbent_count": 5},
                "timing": {"urgency": 0.6, "catalysts": ["launch"]},
                "risks": [{"description": "competition", "severity": 0.4}],
                "effort": {"months": 5, "cost_usd": 30000},
            },
            {"id": "thin", "title": "Thin record"},
        ]
    )
    assert result.ingested == 2
    assert result.scored == 2
    assert result.skipped == 0
    stored = {score.record_id: score for score in pipeline.store.list_scores()}
    assert stored["full"].adjusted_score != 50
    assert stored["thin"].adjusted_score == 0
    assert stored["thin"].missing_fields


def test_pipeline_file_and_partial_errors(tmp_path: Path) -> None:
    path = tmp_path / "records.json"
    path.write_text('[{"title": "Good"}, {"title": ""}]', encoding="utf-8")
    pipeline = Pipeline(Store(tmp_path / "forge.db"))
    result = pipeline.run_file(path)
    assert result.ingested == 1
    assert result.scored == 1
    assert result.skipped == 1
    assert result.errors

    missing = pipeline.run_file(tmp_path / "absent.json")
    assert missing.ingested == 0
    assert missing.scored == 0
    assert missing.errors
