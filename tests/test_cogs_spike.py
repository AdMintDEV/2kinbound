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
    call_line_items,
    cap_usd,
    cogs_ratio,
    estimate_p95_run_usd,
    estimate_tokens,
    evaluate_gate,
    mean_input_tokens,
    monthly_cogs_usd,
    run_cost_usd,
    scoring_call_cost,
    visibility_call_cost,
)
from cogs_spike.engines import (
    CANDIDATE_ENGINES,
    DROPPED_ENGINES,
    SCORING_ENGINE,
    get_engine,
)
from cogs_spike.harness import build_results, write_outputs
from cogs_spike.prompts import DEFAULT_BRAND, render_prompt


def test_research_shortlist_is_three_and_lock_is_two() -> None:
    assert [e.engine_id for e in CANDIDATE_ENGINES] == [
        "openai-web-search",
        "perplexity-sonar",
        "perplexity-agent-web",
    ]
    assert [e.engine_id for e in ALLOWED_ENGINES] == [
        "openai-web-search",
        "perplexity-sonar",
    ]
    assert 1 <= len(ALLOWED_ENGINES) <= 3
    assert [e.engine_id for e in DROPPED_ENGINES] == ["perplexity-agent-web"]
    assert all(e.citation_native for e in ALLOWED_ENGINES)
    for engine in ALLOWED_ENGINES:
        assert engine.model
        assert engine.api
        assert engine.pricing_source.startswith("http")
        assert engine.why


def test_twenty_b2b_prompts_render() -> None:
    assert len(PILOT_PROMPTS) == 20
    for template in PILOT_PROMPTS:
        text = render_prompt(template, DEFAULT_BRAND)
        assert "{" not in text
        assert text


def test_token_estimate_is_deterministic() -> None:
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2
    assert mean_input_tokens() == mean_input_tokens()
    assert mean_input_tokens() > 50


def test_openai_web_search_line_items_match_research_table() -> None:
    engine = get_engine("openai-web-search")
    tokens = TokenUse(199, 280)
    items = call_line_items(engine, tokens)
    by_name = {i.component: i for i in items}
    assert by_name["request_or_tool_fee"].total_usd == pytest.approx(0.01)
    assert by_name["request_or_tool_fee"].basis == "FACT_LIST_PRICE"
    assert by_name["search_content_tokens"].quantity == 8000
    assert by_name["search_content_tokens"].total_usd == pytest.approx(8000 * 0.15 / 1e6)
    assert by_name["prompt_tokens"].total_usd == pytest.approx(199 * 0.15 / 1e6)
    assert by_name["output_tokens"].total_usd == pytest.approx(280 * 0.60 / 1e6)
    cost = call_cost_usd(engine, tokens)
    assert cost.total_usd == pytest.approx(sum(i.total_usd for i in items))
    assert cost.cost_basis == "ESTIMATE"
    assert cost.request_fee_usd == 0.01


def test_sonar_low_context_matches_research_sample_shape() -> None:
    engine = get_engine("perplexity-sonar")
    # Docs sample: 9 in / 402 out + $0.005 ≈ $0.00542
    cost = visibility_call_cost(engine, input_tokens=9, output_tokens=402)
    assert cost.request_fee_usd == 0.005
    assert cost.total_usd == pytest.approx(0.005 + (9 + 402) / 1e6)
    assert abs(cost.total_usd - 0.005411) < 1e-6


def test_run_is_20_prompts_times_locked_engines_plus_scoring() -> None:
    planned_in = 200
    cost, calls, basis = run_cost_usd(
        input_tokens=planned_in,
        output_tokens=100,
        include_scoring=True,
    )
    vis = calls[:2]
    scoring = calls[2]
    expected_vis = 20 * sum(c.total_usd for c in vis)
    assert len(vis) == 2
    assert scoring.engine_id == SCORING_ENGINE.engine_id
    assert cost == pytest.approx(expected_vis + scoring.total_usd)
    assert basis == "ESTIMATE"

    no_score, no_score_calls, _ = run_cost_usd(
        input_tokens=planned_in,
        output_tokens=100,
        include_scoring=False,
    )
    assert len(no_score_calls) == 2
    assert no_score == pytest.approx(expected_vis)


def test_measured_tokens_override_and_label_mixed() -> None:
    measured = {
        "openai-web-search": TokenUse(10, 5),
        "perplexity-sonar": TokenUse(10, 5),
    }
    cost, calls, basis = run_cost_usd(
        measured_by_engine=measured,
        include_scoring=True,
    )
    assert all(c.cost_basis == "MEASURED" for c in calls[:2])
    assert calls[2].cost_basis == "ESTIMATE"
    assert basis == "MIXED"
    assert cost > 0

    cost_m, _, basis_m = run_cost_usd(
        measured_by_engine=measured,
        include_scoring=False,
    )
    assert basis_m == "MEASURED"
    assert cost_m == pytest.approx(20 * sum(c.total_usd for c in calls[:2]))


def test_rejects_more_than_three_engines_or_wrong_prompt_count() -> None:
    with pytest.raises(ValueError, match="at most 3"):
        run_cost_usd(engines=CANDIDATE_ENGINES + ALLOWED_ENGINES[:1])
    with pytest.raises(ValueError, match="20 prompts"):
        run_cost_usd(prompt_count=19)


def test_brand_runs_and_monthly_cogs() -> None:
    limits = StarterLimits(
        on_demand_audits_per_month=2,
        scheduled_rechecks_per_month=4,
        competitors_tracked=2,
    )
    assert brand_runs_per_month(limits) == (1 + 2) * (2 + 4) == 18
    assert monthly_cogs_usd(0.10, limits) == pytest.approx(1.80)
    assert cap_usd(29.0, 0.30) == pytest.approx(8.70)
    assert cogs_ratio(1.80, 29.0) == pytest.approx(1.80 / 29.0)


def test_recommended_starter_passes_estimated_run() -> None:
    cost, _, basis = run_cost_usd()
    assert basis == "ESTIMATE"
    gate = evaluate_gate(cost, RECOMMENDED_STARTER)
    assert gate.passed is True
    assert gate.monthly_cogs_usd < LIST_PRICE_USD * COGS_CAP_RATIO
    assert gate.brand_runs_per_month == 18
    assert RECOMMENDED_STARTER.on_demand_audits_per_month == 2
    assert RECOMMENDED_STARTER.scheduled_rechecks_per_month == 4
    assert RECOMMENDED_STARTER.competitors_tracked == 2


def test_three_candidate_engines_fail_24_brand_runs() -> None:
    cost3, _, basis = run_cost_usd(engines=CANDIDATE_ENGINES)
    assert basis == "ESTIMATE"
    fat = StarterLimits(
        on_demand_audits_per_month=4,
        scheduled_rechecks_per_month=4,
        competitors_tracked=2,
    )
    assert brand_runs_per_month(fat) == 24
    gate = evaluate_gate(cost3, fat)
    assert gate.passed is False
    assert monthly_cogs_usd(cost3, fat) >= 8.70


def test_p95_estimate_is_higher_than_mean_and_still_labeled_estimate() -> None:
    mean, _, basis = run_cost_usd()
    p95 = estimate_p95_run_usd()
    assert basis == "ESTIMATE"
    assert p95 > mean
    assert evaluate_gate(p95, RECOMMENDED_STARTER).passed is True


def test_gate_fails_when_run_is_too_expensive() -> None:
    # 18 runs * $0.50 = $9.00 > $8.70
    gate = evaluate_gate(0.50, RECOMMENDED_STARTER)
    assert gate.passed is False
    assert gate.fail_reasons
    assert "8.70" in gate.fail_reasons[0] or "30%" in gate.fail_reasons[0]
    # 8 min runs * $0.50 = $4.00 < $5.70
    assert any("19.00" in r or "$19" in r for r in gate.fail_reasons)


def test_gate_fails_even_floor_when_impossible() -> None:
    gate = evaluate_gate(1.00, RECOMMENDED_STARTER)
    assert gate.passed is False
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


def test_fail_criteria_reject_list_price_as_measured() -> None:
    text = " ".join(FAIL_CRITERIA).lower()
    assert "30%" in " ".join(FAIL_CRITERIA)
    assert "measured" in text
    assert "research/04" in text or "list price" in text
    assert "scrape" in text or "consumer" in text


def test_harness_dry_run_writes_json_csv_and_refuses_measured_label(tmp_path: Path) -> None:
    results = build_results(live_probes=False)
    assert results["cost_basis"] == "ESTIMATE"
    assert results["measured"] is False
    assert results["research_shortlist"] == "research/04_AC0_ENGINE_LIST_PRICES.md"
    assert results["prompt_count"] == 20
    assert results["engine_count"] == 2
    assert results["starter"]["gate_passed"] is True
    assert results["ac0a"] == "PASS"
    assert results["ac0b"] == "TODO"
    assert results["ac2_code_unblocked"] is True
    assert results["ac2_live_unblocked"] is False
    assert results["ac2_unblocked"] is False
    assert results["usd_per_run"] > 0.2  # web_search fees alone are $0.20
    names = {row["engine_id"] for row in results["engines"]}
    assert names == {"openai-web-search", "perplexity-sonar"}
    openai = next(r for r in results["engines"] if r["engine_id"] == "openai-web-search")
    assert any(i["component"] == "request_or_tool_fee" for i in openai["line_items"])
    json_path, csv_path = write_outputs(results, tmp_path)
    assert json_path.is_file()
    csv_text = csv_path.read_text(encoding="utf-8")
    assert "openai-web-search" in csv_text
    assert "RUN_TOTAL" in csv_text
    assert "MEASURED" not in csv_text.split("RUN_TOTAL")[1]


def test_scoring_is_not_a_visibility_engine() -> None:
    scoring = scoring_call_cost()
    assert scoring.engine_id == "openai-scoring-roll-up"
    assert scoring.engine_id not in {e.engine_id for e in ALLOWED_ENGINES}
    assert scoring.total_usd < 0.01


def test_planned_output_tokens_are_the_documented_budget() -> None:
    assert PLANNED_OUTPUT_TOKENS == 280
