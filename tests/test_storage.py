from pathlib import Path

from forge.models import ResearchRecord
from forge.scoring import score_record
from forge.storage import Store


def test_upsert_and_fetch(tmp_path: Path) -> None:
    store = Store(tmp_path / "forge.db")
    record = ResearchRecord(id="abc123", title="Alpha")
    store.upsert_record(record)
    store.upsert_score(score_record(record))

    loaded = store.get_record("abc123")
    assert loaded is not None
    assert loaded.title == "Alpha"
    assert store.get_score("abc123") is not None
    assert store.get_record("missing") is None
    assert store.get_score("missing") is None
    assert len(store.list_records()) == 1
    assert store.scored_pairs()[0][0].id == "abc123"


def test_scores_sort_descending(tmp_path: Path) -> None:
    store = Store(tmp_path / "forge.db")
    weak = ResearchRecord(id="weak", title="Weak")
    strong = ResearchRecord(
        id="strong",
        title="Strong",
        market={"tam_usd": 3_000_000_000, "growth_rate": 0.3},
        traction={"users": 80_000, "revenue_usd": 4_000_000, "growth_rate": 0.4},
        competition={"intensity": 0.2, "incumbent_count": 1},
        timing={"urgency": 0.8, "catalysts": ["now"]},
        risks=[{"description": "ok", "severity": 0.2}],
        effort={"months": 3, "cost_usd": 10000},
    )
    store.upsert_record(weak)
    store.upsert_record(strong)
    store.upsert_score(score_record(weak))
    store.upsert_score(score_record(strong))
    ranked = store.list_scores()
    assert ranked[0].record_id == "strong"
    assert ranked[0].adjusted_score >= ranked[1].adjusted_score
