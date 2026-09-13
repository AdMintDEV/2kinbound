"""Unit tests for AC#0 COGS math. No network."""

from __future__ import annotations

from pathlib import Path

import pytest

from cogs_spike.calculator import (
    ALLOWED_ENGINES,
    COGS_CAP_RATIO,
    FAIL_CRITERIA,
    LIST_PRICE_USD,
    MINIMUM_VIABLE_STARTER,
    PILOT_PROMPTS,
    PLANNED_OUTPUT_TOKENS,
    PRICE_FLOOR_USD,
    RECOMMENDED_STARTER,
    StarterLimits,
    TokenUse,
    brand_runs_per_month,
    call_cost_usd,
    cap_usd,
    cogs_ratio,
    estimate_tokens,
    evaluate_gate,
    mean_input_tokens,
    monthly_cogs_usd,
    run_cost_usd,
    scoring_call_cost,
    visibility_call_cost,
)
from cogs_spike.engines import get_engine
from cogs_spike.harness import build_results, write_outputs
from cogs_spike.prompts import DEFAULT_BRAND, render_prompt


def test_exactly_three_named_engines() -> None:
    assert 1 <= len(ALLOWED_ENGINES) <= 3
    ids = [e.engine_id for e in ALLOWED_ENGINES]
    assert ids == [
        "openai:gpt-4.1-nano",
        "google:gemini-2.5-flash-lite",
        "perplexity:perplexity/sonar+web_search",
    ]
    assert {e.provider for e in ALLOWED_ENGINES} == {"OpenAI", "Google", "Perplexity"}
    assert any(e.citation_native for e in ALLOWED_ENGINES)
    for engine in ALLOWED_ENGINES:
        assert engine.model
        assert engine.api
        assert engine.pricing_source.startswith("http")
        assert engine.why
        assert engine.input_usd_per_1m >= 0
        assert engine.output_usd_per_1m >= 0


def test_twenty_b2b_prompts_render() -> None:
    assert len(PILOT_PROMPTS) == 20
    for template in PILOT_PROMPTS:
        text = render_prompt(template, DEFAULT_BRAND)
        assert "{" not in text
        assert text
    assert any("category" in t for t in PILOT_PROMPTS)
    assert any("{brand}" in t for t in PILOT_PROMPTS)


def test_token_estimate_is_deterministic() -> None:
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2
    assert estimate_tokens("abcdefgh") == 2
    assert mean_input_tokens() == mean_input_tokens()
    assert mean_input_tokens() > 50


def test_call_cost_matches_list_price_formula() -> None:
    engine = get_engine("openai:gpt-4.1-nano")
    cost = call_cost_usd(engine, TokenUse(1_000_000, 1_000_000))
    assert cost.token_cost_usd == pytest.approx(0.10 + 0.40)
    assert cost.request_fee_usd == 0.0
    assert cost.total_usd == pytest.approx(0.50)
    assert cost.cost_basis == "ESTIMATE"


def test_perplexity_request_fee_dominates_small_calls() -> None:
    engine = get_engine("perplexity:perplexity/sonar+web_search")
    cost = visibility_call_cost(engine, input_tokens=400, output_tokens=280)
    expected_tokens = (400 * 0.25 + 280 * 2.50) / 1_000_000
    assert cost.request_fee_usd == 0.0025
    assert cost.token_cost_usd == pytest.approx(expected_tokens)
    assert cost.total_usd == pytest.approx(expected_tokens + 0.0025)
    assert cost.request_fee_usd > cost.token_cost_usd


def test_run_is_20_prompts_times_engines_plus_scoring() -> None:
    planned_in = 200
    cost, calls, basis = run_cost_usd(
        input_tokens=planned_in,
        output_tokens=100,
        include_scoring=True,
    )
    vis = calls[:3]
    scoring = calls[3]
    expected_vis = 20 * sum(c.total_usd for c in vis)
    assert len(vis) == 3
    assert scoring.engine_id == "openai:gpt-4.1-nano"
    assert cost == pytest.approx(expected_vis + scoring.total_usd)
    assert basis == "ESTIMATE"

    no_score, no_score_calls, _ = run_cost_usd(
        input_tokens=planned_in,
        output_tokens=100,
        include_scoring=False,
    )
    assert len(no_score_calls) == 3
    assert no_score == pytest.approx(expected_vis)


def test_measured_tokens_override_and_label_mixed() -> None:
    measured = {
        "openai:gpt-4.1-nano": TokenUse(10, 5),
        "google:gemini-2.5-flash-lite": TokenUse(10, 5),
        "perplexity:perplexity/sonar+web_search": TokenUse(10, 5),
    }
    cost, calls, basis = run_cost_usd(
        measured_by_engine=measured,
        include_scoring=True,
    )
    assert all(c.cost_basis == "MEASURED" for c in calls[:3])
    assert calls[3].cost_basis == "ESTIMATE"
    assert basis == "MIXED"
    assert cost > 0

    cost_m, _, basis_m = run_cost_usd(
        measured_by_engine=measured,
        include_scoring=False,
    )
    assert basis_m == "MEASURED"
    assert cost_m == pytest.approx(20 * sum(c.total_usd for c in calls[:3]))


def test_rejects_more_than_three_engines_or_wrong_prompt_count() -> None:
    with pytest.raises(ValueError, match="at most 3"):
        run_cost_usd(engines=ALLOWED_ENGINES + ALLOWED_ENGINES[:1])
    with pytest.raises(ValueError, match="20 prompts"):
        run_cost_usd(prompt_count=19)


def test_brand_runs_and_monthly_cogs() -> None:
    limits = StarterLimits(
        on_demand_audits_per_month=4,
        scheduled_rechecks_per_month=4,
        competitors_tracked=2,
    )
    assert brand_runs_per_month(limits) == (1 + 2) * (4 + 4) == 24
    assert monthly_cogs_usd(0.10, limits) == pytest.approx(2.40)
    assert cogs_ratio(2.40, 29.0) == pytest.approx(2.40 / 29.0)
    assert cap_usd(29.0, 0.30) == pytest.approx(8.70)


def test_recommended_starter_passes_estimated_run() -> None:
    cost, _, basis = run_cost_usd()
    assert basis == "ESTIMATE"
    gate = evaluate_gate(cost, RECOMMENDED_STARTER)
    assert gate.passed is True
    assert gate.monthly_cogs_usd < LIST_PRICE_USD * COGS_CAP_RATIO
    assert gate.brand_runs_per_month == 24
    assert RECOMMENDED_STARTER.list_price_usd == 29.0
    assert RECOMMENDED_STARTER.competitors_tracked == 2


def test_gate_fails_when_run_is_too_expensive() -> None:
    # 24 runs * $0.40 = $9.60 > $8.70
    gate = evaluate_gate(0.40, RECOMMENDED_STARTER)
    assert gate.passed is False
    assert gate.fail_reasons
    assert "8.70" in gate.fail_reasons[0] or "30%" in gate.fail_reasons[0]
    # $0.40 still fits minimum-viable at $19 (8 runs * 0.40 = 3.20 < 5.70)
    assert any("19.00" in r or "$19" in r for r in gate.fail_reasons)


def test_gate_fails_even_floor_when_impossible() -> None:
    # 8 min runs * $1 = $8.00 >= $5.70 floor cap
    gate = evaluate_gate(1.00, RECOMMENDED_STARTER)
    assert gate.passed is False
    assert any("minimum-viable" in r.lower() or "floor" in r.lower() for r in gate.fail_reasons)
    min_monthly = monthly_cogs_usd(1.00, MINIMUM_VIABLE_STARTER)
    assert min_monthly >= PRICE_FLOOR_USD * COGS_CAP_RATIO


def test_negative_inputs_rejected() -> None:
    engine = ALLOWED_ENGINES[0]
    with pytest.raises(ValueError):
        call_cost_usd(engine, TokenUse(-1, 0))
    with pytest.raises(ValueError):
        monthly_cogs_usd(-0.01, RECOMMENDED_STARTER)
    with pytest.raises(ValueError):
        cogs_ratio(1.0, 0.0)


def test_fail_criteria_are_explicit() -> None:
    text = " ".join(FAIL_CRITERIA).lower()
    assert "30%" in " ".join(FAIL_CRITERIA)
    assert "ac#2" in text
    assert "$29" in " ".join(FAIL_CRITERIA)
    assert "citation" in text


def test_harness_dry_run_writes_json_csv(tmp_path: Path) -> None:
    results = build_results(live_probes=False)
    assert results["cost_basis"] == "ESTIMATE"
    assert results["prompt_count"] == 20
    assert results["engine_count"] == 3
    assert results["starter"]["gate_passed"] is True
    assert results["ac2_unblocked"] is True
    assert results["usd_per_run"] > 0
    names = {row["engine_id"] for row in results["engines"]}
    assert names == {e.engine_id for e in ALLOWED_ENGINES}
    json_path, csv_path = write_outputs(results, tmp_path)
    assert json_path.is_file()
    assert csv_path.is_file()
    csv_text = csv_path.read_text(encoding="utf-8")
    assert "openai:gpt-4.1-nano" in csv_text
    assert "RUN_TOTAL" in csv_text


def test_scoring_is_not_a_fourth_engine() -> None:
    scoring = scoring_call_cost()
    assert scoring.engine_id in {e.engine_id for e in ALLOWED_ENGINES}
    assert scoring.total_usd < 0.01


def test_planned_output_tokens_are_the_documented_budget() -> None:
    assert PLANNED_OUTPUT_TOKENS == 280
