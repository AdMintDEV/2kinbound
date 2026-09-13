#!/usr/bin/env python3
"""AC#0 COGS harness.

Uses research/04_AC0_ENGINE_LIST_PRICES.md as the shortlist + list-price table.
Dry-runs that table when API keys are absent. Live probes are opt-in (`--live`)
because OpenAI web_search costs $0.01/call. Writes JSON + CSV.

List prices are FACT. $/run is ESTIMATE unless provider usage is attached.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from cogs_spike.calculator import (  # type: ignore[no-redef]
        COGS_CAP_RATIO,
        FAIL_CRITERIA,
        FREE_AUDITS_PER_IP_PER_DAY,
        LIST_PRICE_USD,
        PLANNED_OUTPUT_TOKENS,
        RECOMMENDED_STARTER,
        TokenUse,
        estimate_p95_run_usd,
        evaluate_gate,
        mean_input_tokens,
        monthly_cogs_usd,
        run_cost_usd,
    )
    from cogs_spike.engines import (
        ALLOWED_ENGINES,
        CANDIDATE_ENGINES,
        DROPPED_ENGINES,
        RESEARCH_PRICE_DOC,
    )
    from cogs_spike.prompts import DEFAULT_BRAND, PILOT_PROMPTS, SYSTEM_PROMPT
else:
    from .calculator import (
        COGS_CAP_RATIO,
        FAIL_CRITERIA,
        FREE_AUDITS_PER_IP_PER_DAY,
        LIST_PRICE_USD,
        PLANNED_OUTPUT_TOKENS,
        RECOMMENDED_STARTER,
        TokenUse,
        estimate_p95_run_usd,
        evaluate_gate,
        mean_input_tokens,
        monthly_cogs_usd,
        run_cost_usd,
    )
    from .engines import (
        ALLOWED_ENGINES,
        CANDIDATE_ENGINES,
        DROPPED_ENGINES,
        RESEARCH_PRICE_DOC,
    )
    from .prompts import DEFAULT_BRAND, PILOT_PROMPTS, SYSTEM_PROMPT

RESULTS_DIR = Path(__file__).resolve().parent / "results"
JSON_NAME = "ac0_pilot_results.json"
CSV_NAME = "ac0_pilot_results.csv"
PROBE_USER_PROMPT = "Reply with the single word ok."


def present_keys() -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for engine in CANDIDATE_ENGINES:
        value = next((os.environ.get(name) for name in engine.env_keys if os.environ.get(name)), None)
        found[engine.engine_id] = value
    return found


def _json_request(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def probe_openai_web_search(api_key: str, timeout: float) -> TokenUse:
    data = _json_request(
        "https://api.openai.com/v1/responses",
        {
            "model": "gpt-4o-mini",
            "tools": [{"type": "web_search"}],
            "input": PROBE_USER_PROMPT,
            "max_output_tokens": 16,
        },
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        timeout,
    )
    usage = data.get("usage") or {}
    return TokenUse(
        input_tokens=int(usage.get("input_tokens") or usage.get("prompt_tokens") or 0),
        output_tokens=int(usage.get("output_tokens") or usage.get("completion_tokens") or 0),
    )


def probe_sonar(api_key: str, timeout: float) -> TokenUse:
    data = _json_request(
        "https://api.perplexity.ai/chat/completions",
        {
            "model": "sonar",
            "messages": [{"role": "user", "content": PROBE_USER_PROMPT}],
            "max_tokens": 8,
            "web_search_options": {"search_context_size": "low"},
        },
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        timeout,
    )
    usage = data.get("usage") or {}
    return TokenUse(
        input_tokens=int(usage.get("prompt_tokens") or 0),
        output_tokens=int(usage.get("completion_tokens") or 0),
    )


PROBES = {
    "openai-web-search": probe_openai_web_search,
    "perplexity-sonar": probe_sonar,
}


def run_live_probes(
    keys: dict[str, str | None],
    *,
    timeout: float = 20.0,
    enabled: bool = False,
) -> dict[str, Any]:
    """Opt-in. OpenAI web_search is $0.01/call — not a free-tier probe."""
    report: dict[str, Any] = {}
    for engine in ALLOWED_ENGINES:
        key = keys.get(engine.engine_id)
        if not enabled:
            report[engine.engine_id] = {
                "status": "skipped",
                "reason": "live_opt_in_only",
                "note": "Pass --live to spend ~$0.01+ per OpenAI web_search probe",
            }
            continue
        if not key:
            report[engine.engine_id] = {"status": "skipped", "reason": "no_api_key"}
            continue
        probe = PROBES.get(engine.engine_id)
        if probe is None:
            report[engine.engine_id] = {"status": "skipped", "reason": "no_probe"}
            continue
        try:
            tokens = probe(key, timeout)
            report[engine.engine_id] = {
                "status": "ok",
                "input_tokens": tokens.input_tokens,
                "output_tokens": tokens.output_tokens,
                "note": (
                    "1-call connectivity probe. Token counts here are NOT the "
                    "20-prompt budget and do not make $/run MEASURED."
                ),
            }
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, ValueError) as exc:
            report[engine.engine_id] = {"status": "error", "reason": str(exc)}
    return report


def _engine_row(engine, call, keys, probes) -> dict[str, Any]:
    return {
        "engine_id": engine.engine_id,
        "provider": engine.provider,
        "model": engine.model,
        "api": engine.api,
        "endpoint": engine.endpoint,
        "citation_native": engine.citation_native,
        "research_role": engine.research_role,
        "input_usd_per_1m": engine.input_usd_per_1m,
        "output_usd_per_1m": engine.output_usd_per_1m,
        "request_fee_usd": engine.request_fee_usd,
        "extra_input_tokens": engine.extra_input_tokens,
        "pricing_source": engine.pricing_source,
        "pricing_as_of": engine.pricing_as_of,
        "planned_prompt_tokens": call.tokens.input_tokens,
        "planned_output_tokens": call.tokens.output_tokens,
        "billed_input_tokens": call.billed_input_tokens,
        "usd_per_call": round(call.total_usd, 8),
        "usd_per_run_20_prompts": round(call.total_usd * 20, 8),
        "cost_basis": call.cost_basis,
        "line_items": [item.to_dict() for item in call.line_items],
        "why": engine.why,
        "tradeoff": engine.tradeoff,
        "env_keys": list(engine.env_keys),
        "key_present": bool(keys.get(engine.engine_id)),
        "live_probe": probes.get(engine.engine_id, {"status": "skipped"}),
    }


def build_results(
    *,
    live_probes: bool = False,
    output_tokens: int = PLANNED_OUTPUT_TOKENS,
) -> dict[str, Any]:
    keys = present_keys()
    probes = run_live_probes(keys, enabled=live_probes)
    planned_in = mean_input_tokens()
    cost, per_call, basis = run_cost_usd(
        input_tokens=planned_in,
        output_tokens=output_tokens,
    )
    p95 = estimate_p95_run_usd(input_tokens=planned_in)
    gate = evaluate_gate(cost, RECOMMENDED_STARTER)
    limits = RECOMMENDED_STARTER

    three_engine_cost, _, _ = run_cost_usd(
        engines=CANDIDATE_ENGINES,
        input_tokens=planned_in,
        output_tokens=output_tokens,
    )
    three_at_recommended = monthly_cogs_usd(three_engine_cost, limits)
    three_at_24 = monthly_cogs_usd(
        three_engine_cost,
        type(limits)(
            on_demand_audits_per_month=4,
            scheduled_rechecks_per_month=4,
            competitors_tracked=2,
        ),
    )

    visibility_calls = per_call[: len(ALLOWED_ENGINES)]
    scoring_call = per_call[len(ALLOWED_ENGINES) :]
    engines_out = [
        _engine_row(engine, call, keys, probes)
        for engine, call in zip(ALLOWED_ENGINES, visibility_calls, strict=True)
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": "Inbound Score",
        "ac": "AC#0",
        "research_shortlist": RESEARCH_PRICE_DOC,
        "cost_basis": basis,
        "measured": False,
        "cost_basis_note": (
            "ESTIMATE = FACT list prices from research/04 × ESTIMATE token "
            "quantities (4 chars/token) + FACT per-call fees + FACT 8k OpenAI "
            "search-content block. This is NOT a measured $/run. MEASURED "
            "requires provider usage on the 20-prompt set or an invoice export."
        ),
        "run_definition": (
            "One run = one brand URL × 20 prompts × the locked engines "
            f"({', '.join(e.engine_id for e in ALLOWED_ENGINES)}), "
            "plus one gpt-4o-mini scoring roll-up (not a visibility engine). "
            "Each tracked competitor is an extra run of the same 20×N set."
        ),
        "prompt_count": len(PILOT_PROMPTS),
        "engine_count": len(ALLOWED_ENGINES),
        "candidates": [
            {
                "engine_id": e.engine_id,
                "research_role": e.research_role,
                "model": e.model,
                "api": e.api,
                "request_fee_usd": e.request_fee_usd,
            }
            for e in CANDIDATE_ENGINES
        ],
        "dropped": [
            {
                "engine_id": e.engine_id,
                "reason": e.tradeoff,
                "usd_per_run_if_kept_estimate": round(three_engine_cost, 8),
                "monthly_cogs_at_recommended_limits": round(three_at_recommended, 8),
                "monthly_cogs_at_24_brand_runs": round(three_at_24, 8),
                "would_fail_30pct_at_24_runs": three_at_24 >= LIST_PRICE_USD * COGS_CAP_RATIO,
            }
            for e in DROPPED_ENGINES
        ],
        "brand_fixture": {
            "brand": DEFAULT_BRAND.brand,
            "url": DEFAULT_BRAND.url,
            "category": DEFAULT_BRAND.category,
            "competitor": DEFAULT_BRAND.competitor,
            "note": "Fixture for token shape only. Not a real audit. No citations invented.",
        },
        "prompts": list(PILOT_PROMPTS),
        "system_prompt": SYSTEM_PROMPT,
        "planned_mean_input_tokens": planned_in,
        "planned_output_tokens": output_tokens,
        "engines": engines_out,
        "scoring_roll_up": (
            {
                "engine_id": scoring_call[0].engine_id,
                "usd": round(scoring_call[0].total_usd, 8),
                "input_tokens": scoring_call[0].tokens.input_tokens,
                "output_tokens": scoring_call[0].tokens.output_tokens,
                "cost_basis": scoring_call[0].cost_basis,
                "note": "Scoring is not a visibility engine.",
            }
            if scoring_call
            else None
        ),
        "usd_per_run": round(cost, 8),
        "usd_per_run_p95_estimate": round(p95, 8),
        "usd_per_run_note": (
            "mean = baseline ESTIMATE; p95_estimate = Sonar medium fee "
            "($0.008) + 1.5× output tokens. Neither is measured."
        ),
        "starter": {
            "list_price_usd": limits.list_price_usd,
            "on_demand_audits_per_month": limits.on_demand_audits_per_month,
            "scheduled_rechecks_per_month": limits.scheduled_rechecks_per_month,
            "competitors_tracked": limits.competitors_tracked,
            "brand_runs_per_month": gate.brand_runs_per_month,
            "monthly_cogs_usd": round(gate.monthly_cogs_usd, 8),
            "monthly_cogs_p95_estimate_usd": round(p95 * gate.brand_runs_per_month, 8),
            "cogs_ratio": round(gate.cogs_ratio, 6),
            "cogs_cap_ratio": COGS_CAP_RATIO,
            "cogs_cap_usd": round(gate.cap_usd, 4),
            "gate_passed": gate.passed,
            "fail_reasons": list(gate.fail_reasons),
        },
        "free_audit": {
            "audits_per_ip_per_day": FREE_AUDITS_PER_IP_PER_DAY,
            "uses_locked_engine_set": True,
            "usd_per_audit_estimate": round(cost, 8),
            "note": "Marketing COGS, not Starter subscriber COGS. Same 20×N run.",
        },
        "fail_criteria": list(FAIL_CRITERIA),
        "ac0a": "PASS" if gate.passed else "FAIL",
        "ac0b": "TODO",
        "ac2_code_unblocked": bool(gate.passed),
        "ac2_live_unblocked": False,
        "ac2_unblocked": False,
        "ac2_note": (
            "AC#0a allows implementing free-audit code on the frozen engine IDs. "
            "LAUNCH and live free-audit traffic require AC#0b. Not fully unblocked."
        ),
        "list_price_usd": LIST_PRICE_USD,
    }


def write_outputs(results: dict[str, Any], directory: Path = RESULTS_DIR) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    json_path = directory / JSON_NAME
    csv_path = directory / CSV_NAME
    json_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "engine_id",
                "provider",
                "model",
                "api",
                "citation_native",
                "usd_per_call",
                "usd_per_run_20_prompts",
                "cost_basis",
                "key_present",
                "live_probe_status",
            ],
        )
        writer.writeheader()
        for row in results["engines"]:
            writer.writerow(
                {
                    "engine_id": row["engine_id"],
                    "provider": row["provider"],
                    "model": row["model"],
                    "api": row["api"],
                    "citation_native": row["citation_native"],
                    "usd_per_call": row["usd_per_call"],
                    "usd_per_run_20_prompts": row["usd_per_run_20_prompts"],
                    "cost_basis": row["cost_basis"],
                    "key_present": row["key_present"],
                    "live_probe_status": (row.get("live_probe") or {}).get("status"),
                }
            )
        writer.writerow(
            {
                "engine_id": "RUN_TOTAL",
                "provider": "",
                "model": "",
                "api": results["run_definition"],
                "citation_native": "",
                "usd_per_call": "",
                "usd_per_run_20_prompts": results["usd_per_run"],
                "cost_basis": results["cost_basis"],
                "key_present": "",
                "live_probe_status": "",
            }
        )
    return json_path, csv_path


def print_summary(results: dict[str, Any]) -> None:
    print("Inbound Score AC#0 — allowed engines")
    print("===================================")
    print(f"Shortlist source: {results['research_shortlist']}")
    print(f"Cost basis: {results['cost_basis']}  measured={results['measured']}")
    for row in results["engines"]:
        print(
            f"- {row['engine_id']}: {row['provider']} {row['model']} via {row['api']}\n"
            f"    $/call={row['usd_per_call']:.6f}  "
            f"$/run={row['usd_per_run_20_prompts']:.6f}  "
            f"basis={row['cost_basis']}"
        )
        for item in row["line_items"]:
            print(
                f"      {item['component']}: qty={item['quantity']} "
                f"→ ${item['total_usd']:.6f} ({item['basis']})"
            )
    print()
    print(f"Run definition: {results['run_definition']}")
    print(f"$/run mean (ESTIMATE): ${results['usd_per_run']:.6f}")
    print(f"$/run p95 (ESTIMATE):  ${results['usd_per_run_p95_estimate']:.6f}")
    starter = results["starter"]
    print(
        "Starter limits: "
        f"{starter['on_demand_audits_per_month']} on-demand audits/mo, "
        f"{starter['scheduled_rechecks_per_month']} scheduled rechecks/mo, "
        f"{starter['competitors_tracked']} competitors "
        f"→ {starter['brand_runs_per_month']} brand-runs/mo"
    )
    print(
        f"Monthly COGS: ${starter['monthly_cogs_usd']:.6f} "
        f"({starter['cogs_ratio']:.2%} of ${starter['list_price_usd']:.2f}; "
        f"cap {starter['cogs_cap_ratio']:.0%} = ${starter['cogs_cap_usd']:.2f})"
    )
    print(f"Gate AC#0a: {'PASS' if starter['gate_passed'] else 'FAIL'}")
    print(f"AC#0b: {results['ac0b']}")
    print(f"AC#2 code unblocked: {results['ac2_code_unblocked']}")
    print(f"AC#2 live unblocked: {results['ac2_live_unblocked']}")
    for dropped in results["dropped"]:
        print(
            f"Dropped {dropped['engine_id']}: 24-run COGS "
            f"${dropped['monthly_cogs_at_24_brand_runs']:.4f} "
            f"(fail 30%={dropped['would_fail_30pct_at_24_runs']})"
        )
    if starter["fail_reasons"]:
        for reason in starter["fail_reasons"]:
            print(f"  FAIL: {reason}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inbound Score AC#0 COGS harness")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Spend ~$0.01+ on optional 1-call probes (requires API keys)",
    )
    parser.add_argument(
        "--no-live",
        action="store_true",
        help="Force dry-run (default)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RESULTS_DIR,
        help="Directory for JSON/CSV (default: product/cogs_spike/results)",
    )
    args = parser.parse_args(argv)
    results = build_results(live_probes=bool(args.live) and not args.no_live)
    json_path, csv_path = write_outputs(results, args.output_dir)
    print_summary(results)
    print()
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")
    return 0 if results["starter"]["gate_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
