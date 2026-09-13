"""Deterministic weighted opportunity scoring with explicit missing-data handling."""

from __future__ import annotations

import math

from forge.models import FactorScore, OpportunityScore, ResearchRecord

WEIGHTS: dict[str, float] = {
    "market": 0.25,
    "traction": 0.20,
    "competition": 0.15,
    "timing": 0.15,
    "risk": 0.15,
    "effort": 0.10,
}

assert math.isclose(sum(WEIGHTS.values()), 1.0, abs_tol=1e-9)


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _log_scale(value: float, midpoint: float) -> float:
    """Map a positive quantity onto 0-100 using a logistic-like log curve."""
    if value <= 0:
        return 0.0
    return _clamp(100.0 * math.log10(1.0 + value / midpoint) / math.log10(1.0 + 100.0))


def _growth_score(rate: float) -> float:
    return _clamp(40.0 + 120.0 * rate)


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def score_market(record: ResearchRecord) -> FactorScore:
    missing: list[str] = []
    parts: list[float] = []
    notes: list[str] = []
    market = record.market

    if market.tam_usd is None:
        missing.append("market.tam_usd")
    else:
        parts.append(_log_scale(market.tam_usd, 10_000_000))
        notes.append(f"TAM ${market.tam_usd:,.0f}")

    if market.growth_rate is None:
        missing.append("market.growth_rate")
    else:
        parts.append(_growth_score(market.growth_rate))
        notes.append(f"growth {market.growth_rate:.0%}")

    value = _mean(parts)
    rationale = "; ".join(notes) if notes else "no market signals"
    return FactorScore(
        name="market",
        weight=WEIGHTS["market"],
        value=value,
        missing_fields=missing,
        rationale=rationale,
    )


def score_traction(record: ResearchRecord) -> FactorScore:
    missing: list[str] = []
    parts: list[float] = []
    notes: list[str] = []
    traction = record.traction

    if traction.revenue_usd is None:
        missing.append("traction.revenue_usd")
    else:
        parts.append(_log_scale(traction.revenue_usd, 100_000))
        notes.append(f"revenue ${traction.revenue_usd:,.0f}")

    if traction.users is None:
        missing.append("traction.users")
    else:
        parts.append(_log_scale(float(traction.users), 1_000))
        notes.append(f"{traction.users:,} users")

    if traction.growth_rate is None:
        missing.append("traction.growth_rate")
    else:
        parts.append(_growth_score(traction.growth_rate))
        notes.append(f"growth {traction.growth_rate:.0%}")

    value = _mean(parts)
    rationale = "; ".join(notes) if notes else "no traction signals"
    return FactorScore(
        name="traction",
        weight=WEIGHTS["traction"],
        value=value,
        missing_fields=missing,
        rationale=rationale,
    )


def score_competition(record: ResearchRecord) -> FactorScore:
    missing: list[str] = []
    parts: list[float] = []
    notes: list[str] = []
    competition = record.competition

    if competition.intensity is None:
        missing.append("competition.intensity")
    else:
        parts.append(_clamp(100.0 * (1.0 - competition.intensity)))
        notes.append(f"intensity {competition.intensity:.2f}")

    if competition.incumbent_count is None:
        missing.append("competition.incumbent_count")
    else:
        count = competition.incumbent_count
        if count <= 1:
            incumbent_score = 90.0
        elif count <= 3:
            incumbent_score = 70.0
        elif count <= 8:
            incumbent_score = 50.0
        else:
            incumbent_score = 25.0
        parts.append(incumbent_score)
        notes.append(f"{count} incumbents")

    value = _mean(parts)
    rationale = "; ".join(notes) if notes else "no competition signals"
    return FactorScore(
        name="competition",
        weight=WEIGHTS["competition"],
        value=value,
        missing_fields=missing,
        rationale=rationale,
    )


def score_timing(record: ResearchRecord) -> FactorScore:
    missing: list[str] = []
    parts: list[float] = []
    notes: list[str] = []
    timing = record.timing

    if timing.urgency is None:
        missing.append("timing.urgency")
    else:
        parts.append(_clamp(100.0 * timing.urgency))
        notes.append(f"urgency {timing.urgency:.2f}")

    catalyst_count = len([c for c in timing.catalysts if c.strip()])
    if catalyst_count == 0 and timing.urgency is None:
        missing.append("timing.catalysts")
    elif catalyst_count:
        catalyst_score = _clamp(30.0 + 18.0 * catalyst_count)
        parts.append(catalyst_score)
        notes.append(f"{catalyst_count} catalyst(s)")

    value = _mean(parts)
    rationale = "; ".join(notes) if notes else "no timing signals"
    return FactorScore(
        name="timing",
        weight=WEIGHTS["timing"],
        value=value,
        missing_fields=missing,
        rationale=rationale,
    )


def score_risk(record: ResearchRecord) -> FactorScore:
    if not record.risks:
        return FactorScore(
            name="risk",
            weight=WEIGHTS["risk"],
            value=None,
            missing_fields=["risks"],
            rationale="no risks provided; not assumed safe",
        )

    severities = [
        item.severity if hasattr(item, "severity") else float(item["severity"])
        for item in record.risks
    ]
    max_severity = max(severities)
    mean_severity = sum(severities) / len(severities)
    blended = 0.7 * max_severity + 0.3 * mean_severity
    value = _clamp(100.0 * (1.0 - blended))
    return FactorScore(
        name="risk",
        weight=WEIGHTS["risk"],
        value=value,
        missing_fields=[],
        rationale=f"{len(record.risks)} risk(s); max severity {max_severity:.2f}",
    )


def score_effort(record: ResearchRecord) -> FactorScore:
    missing: list[str] = []
    parts: list[float] = []
    notes: list[str] = []
    effort = record.effort

    if effort.months is None:
        missing.append("effort.months")
    else:
        parts.append(_clamp(100.0 * math.exp(-effort.months / 8.0)))
        notes.append(f"{effort.months:g} months")

    if effort.cost_usd is None:
        missing.append("effort.cost_usd")
    else:
        parts.append(_clamp(100.0 * math.exp(-effort.cost_usd / 80_000.0)))
        notes.append(f"cost ${effort.cost_usd:,.0f}")

    value = _mean(parts)
    rationale = "; ".join(notes) if notes else "no effort signals"
    return FactorScore(
        name="effort",
        weight=WEIGHTS["effort"],
        value=value,
        missing_fields=missing,
        rationale=rationale,
    )


FACTOR_SCORERS = (
    score_market,
    score_traction,
    score_competition,
    score_timing,
    score_risk,
    score_effort,
)


def _evidence_boost(record: ResearchRecord) -> float:
    if not record.evidence:
        return 0.0
    strengths = [item.strength for item in record.evidence]
    avg_strength = sum(strengths) / len(strengths)
    coverage = min(1.0, len(record.evidence) / 4.0)
    return 0.08 * avg_strength * coverage


def score_record(record: ResearchRecord) -> OpportunityScore:
    factors = [scorer(record) for scorer in FACTOR_SCORERS]
    present = [factor for factor in factors if factor.value is not None]
    missing_fields = [field for factor in factors for field in factor.missing_fields]

    if present:
        weight_sum = sum(factor.weight for factor in present)
        raw = sum(factor.weight * factor.value for factor in present) / weight_sum
    else:
        raw = 50.0

    completeness = len(present) / len(factors)
    boost = _evidence_boost(record)
    completeness = _clamp(completeness + boost, 0.0, 1.0)

    # Missing evidence cannot inflate rank: unknown opportunity scores toward 0.
    adjusted = raw * completeness
    confidence = _clamp(100.0 * completeness * (0.7 + 0.3 * (len(record.evidence) / 4.0)))

    return OpportunityScore(
        record_id=record.id,
        raw_score=round(raw, 2),
        adjusted_score=round(adjusted, 2),
        completeness=round(completeness, 4),
        confidence=round(confidence, 2),
        missing_fields=missing_fields,
        factors=factors,
    )
