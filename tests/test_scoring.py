from forge.models import ResearchRecord, RiskItem
from forge.scoring import WEIGHTS, score_record, score_risk


def _record(**kwargs) -> ResearchRecord:
    return ResearchRecord(title="Test opportunity", **kwargs)


def test_weights_sum_to_one() -> None:
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_complete_record_scores_above_watch() -> None:
    record = _record(
        market={"tam_usd": 2_000_000_000, "growth_rate": 0.25},
        traction={"users": 50_000, "revenue_usd": 2_000_000, "growth_rate": 0.4},
        competition={"intensity": 0.2, "incumbent_count": 2},
        timing={"urgency": 0.8, "catalysts": ["regulation", "new channel"]},
        risks=[{"description": "execution", "severity": 0.3}],
        effort={"months": 4, "cost_usd": 20000},
        evidence=[{"claim": "paid pilots", "strength": 0.9}],
    )
    score = score_record(record)
    assert score.adjusted_score >= 55
    assert score.completeness > 0.9
    assert score.missing_fields == []
    assert score.rank_band() in {"watch", "strong"}


def test_missing_data_cannot_outrank_documented_records() -> None:
    thin = score_record(_record())
    documented = score_record(
        _record(
            market={"tam_usd": 80_000_000, "growth_rate": 0.08},
            traction={"users": 200, "revenue_usd": 12000, "growth_rate": 0.05},
            competition={"intensity": 0.6, "incumbent_count": 8},
            timing={"urgency": 0.3, "catalysts": ["maybe"]},
            risks=[{"description": "crowded", "severity": 0.6}],
            effort={"months": 10, "cost_usd": 90000},
        )
    )
    assert thin.raw_score == 50
    assert thin.adjusted_score == 0
    assert "market.tam_usd" in thin.missing_fields
    assert "risks" in thin.missing_fields
    assert thin.completeness < documented.completeness
    assert thin.confidence < documented.confidence
    assert thin.adjusted_score < documented.adjusted_score


def test_absent_risks_are_missing_not_safe() -> None:
    factor = score_risk(_record())
    assert factor.value is None
    assert factor.missing_fields == ["risks"]


def test_high_risk_lowers_score() -> None:
    base = _record(
        market={"tam_usd": 100_000_000, "growth_rate": 0.2},
        traction={"users": 1000, "revenue_usd": 50000, "growth_rate": 0.1},
        competition={"intensity": 0.4, "incumbent_count": 4},
        timing={"urgency": 0.5, "catalysts": ["pilot"]},
        effort={"months": 6, "cost_usd": 40000},
    )
    risky = base.model_copy(
        update={"risks": [RiskItem(description="fatal", severity=0.95)]}
    )
    safe = base.model_copy(
        update={"risks": [RiskItem(description="minor", severity=0.1)]}
    )
    assert score_record(risky).raw_score < score_record(safe).raw_score


def test_rank_bands() -> None:
    strong = score_record(
        _record(
            market={"tam_usd": 8_000_000_000, "growth_rate": 0.5},
            traction={"users": 500_000, "revenue_usd": 20_000_000, "growth_rate": 0.6},
            competition={"intensity": 0.05, "incumbent_count": 0},
            timing={"urgency": 1.0, "catalysts": ["a", "b", "c"]},
            risks=[{"description": "tiny", "severity": 0.05}],
            effort={"months": 1, "cost_usd": 1000},
            evidence=[
                {"claim": "e1", "strength": 1.0},
                {"claim": "e2", "strength": 1.0},
                {"claim": "e3", "strength": 1.0},
                {"claim": "e4", "strength": 1.0},
            ],
        )
    )
    assert strong.rank_band() == "strong"
    assert score_record(_record()).rank_band() == "pass"
