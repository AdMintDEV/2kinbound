#!/usr/bin/env python3
"""AC#0 COGS harness.

Dry-runs with the recorded public pricing table when API keys are absent.
Optional 1-call live probes when keys exist (near-zero spend). Never scrapes
consumer UIs. Writes JSON + CSV next to the AC#0 doc.
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
        evaluate_gate,
        mean_input_tokens,
        run_cost_usd,
    )
    from cogs_spike.engines import ALLOWED_ENGINES
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
        evaluate_gate,
        mean_input_tokens,
        run_cost_usd,
    )
    from .engines import ALLOWED_ENGINES
    from .prompts import DEFAULT_BRAND, PILOT_PROMPTS, SYSTEM_PROMPT

RESULTS_DIR = Path(__file__).resolve().parent / "results"
JSON_NAME = "ac0_pilot_results.json"
CSV_NAME = "ac0_pilot_results.csv"
PROBE_USER_PROMPT = "Reply with the single word ok."


def present_keys() -> dict[str, str | None]:
    found: dict[str, str | None] = {}
    for engine in ALLOWED_ENGINES:
        value = next((os.environ.get(name) for name in engine.env_keys if os.environ.get(name)), None)
        found[engine.engine_id] = value
    return found


def _json_request(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: float) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def probe_openai(api_key: str, timeout: float) -> TokenUse:
    data = _json_request(
        "https://api.openai.com/v1/chat/completions",
        {
            "model": "gpt-4.1-nano",
            "messages": [
                {"role": "system", "content": "Be brief."},
                {"role": "user", "content": PROBE_USER_PROMPT},
            ],
            "max_tokens": 8,
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


def probe_gemini(api_key: str, timeout: float) -> TokenUse:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash-lite:generateContent?key={api_key}"
    )
    data = _json_request(
        url,
        {
            "contents": [{"parts": [{"text": PROBE_USER_PROMPT}]}],
            "generationConfig": {"maxOutputTokens": 8},
        },
        {"Content-Type": "application/json"},
        timeout,
    )
    usage = data.get("usageMetadata") or {}
    return TokenUse(
        input_tokens=int(usage.get("promptTokenCount") or 0),
        output_tokens=int(usage.get("candidatesTokenCount") or 0),
    )


def probe_perplexity(api_key: str, timeout: float) -> TokenUse:
    data = _json_request(
        "https://api.perplexity.ai/v1/agent",
        {
            "model": "perplexity/sonar",
            "input": PROBE_USER_PROMPT,
            "tools": [{"type": "web_search"}],
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


PROBES = {
    "openai:gpt-4.1-nano": probe_openai,
    "google:gemini-2.5-flash-lite": probe_gemini,
    "perplexity:perplexity/sonar+web_search": probe_perplexity,
}


def run_live_probes(
    keys: dict[str, str | None],
    *,
    timeout: float = 20.0,
    enabled: bool = True,
) -> dict[str, Any]:
    """At most one tiny probe per engine. Skip entirely when no keys."""
    report: dict[str, Any] = {}
    if not enabled:
        return report
    for engine in ALLOWED_ENGINES:
        key = keys.get(engine.engine_id)
        if not key:
            report[engine.engine_id] = {"status": "skipped", "reason": "no_api_key"}
            continue
        probe = PROBES[engine.engine_id]
        try:
            tokens = probe(key, timeout)
            report[engine.engine_id] = {
                "status": "ok",
                "input_tokens": tokens.input_tokens,
                "output_tokens": tokens.output_tokens,
                "note": "1-call connectivity probe only; not used as the 20-prompt token budget",
            }
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, ValueError) as exc:
            report[engine.engine_id] = {"status": "error", "reason": str(exc)}
    return report


def build_results(
    *,
    live_probes: bool = True,
    output_tokens: int = PLANNED_OUTPUT_TOKENS,
) -> dict[str, Any]:
    keys = present_keys()
    probes = run_live_probes(keys, enabled=live_probes)
    planned_in = mean_input_tokens()
    cost, per_call, basis = run_cost_usd(
        input_tokens=planned_in,
        output_tokens=output_tokens,
    )
    gate = evaluate_gate(cost, RECOMMENDED_STARTER)
    limits = RECOMMENDED_STARTER

    engines_out = []
    # First N entries are visibility; last may be scoring with the same OpenAI id.
    visibility_calls = per_call[: len(ALLOWED_ENGINES)]
    scoring_call = per_call[len(ALLOWED_ENGINES) :]
    for engine, call in zip(ALLOWED_ENGINES, visibility_calls, strict=True):
        engines_out.append(
            {
                "engine_id": engine.engine_id,
                "provider": engine.provider,
                "model": engine.model,
                "api": engine.api,
                "endpoint": engine.endpoint,
                "citation_native": engine.citation_native,
                "input_usd_per_1m": engine.input_usd_per_1m,
                "output_usd_per_1m": engine.output_usd_per_1m,
                "request_fee_usd": engine.request_fee_usd,
                "pricing_source": engine.pricing_source,
                "pricing_as_of": engine.pricing_as_of,
                "planned_input_tokens": call.tokens.input_tokens,
                "planned_output_tokens": call.tokens.output_tokens,
                "usd_per_call": round(call.total_usd, 8),
                "usd_per_run_20_prompts": round(call.total_usd * 20, 8),
                "cost_basis": call.cost_basis,
                "why": engine.why,
                "tradeoff": engine.tradeoff,
                "env_keys": list(engine.env_keys),
                "key_present": bool(keys.get(engine.engine_id)),
                "live_probe": probes.get(engine.engine_id, {"status": "skipped"}),
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "product": "Inbound Score",
        "ac": "AC#0",
        "cost_basis": basis,
        "cost_basis_note": (
            "ESTIMATE = public list prices × estimated tokens (4 chars/token). "
            "No API keys were required to produce this file. MEASURED appears "
            "only when a provider returns usage for the 20-prompt set."
        ),
        "run_definition": (
            "One run = one brand URL × 20 prompts × the 3 locked engines, "
            "plus one OpenAI gpt-4.1-nano scoring roll-up. "
            "Each tracked competitor is an extra run of the same 20×3 set."
        ),
        "prompt_count": len(PILOT_PROMPTS),
        "engine_count": len(ALLOWED_ENGINES),
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
                "note": "Scoring is not a fourth visibility engine.",
            }
            if scoring_call
            else None
        ),
        "usd_per_run": round(cost, 8),
        "starter": {
            "list_price_usd": limits.list_price_usd,
            "on_demand_audits_per_month": limits.on_demand_audits_per_month,
            "scheduled_rechecks_per_month": limits.scheduled_rechecks_per_month,
            "competitors_tracked": limits.competitors_tracked,
            "brand_runs_per_month": gate.brand_runs_per_month,
            "monthly_cogs_usd": round(gate.monthly_cogs_usd, 8),
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
            "note": "Marketing COGS, not Starter subscriber COGS. Same 20×3 run.",
        },
        "fail_criteria": list(FAIL_CRITERIA),
        "ac2_unblocked": gate.passed,
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
    for row in results["engines"]:
        print(
            f"- {row['provider']} {row['model']} via {row['api']}\n"
            f"    id={row['engine_id']}  $/call={row['usd_per_call']:.6f}  "
            f"$/run={row['usd_per_run_20_prompts']:.6f}  "
            f"basis={row['cost_basis']}  key={row['key_present']}"
        )
    print()
    print(f"Run definition: {results['run_definition']}")
    print(f"$/run ({results['cost_basis']}): ${results['usd_per_run']:.6f}")
    starter = results["starter"]
    print(
        "Starter limits: "
        f"{starter['on_demand_audits_per_month']} on-demand audits/mo, "
        f"{starter['scheduled_rechecks_per_month']} scheduled rechecks/mo, "
        f"{starter['competitors_tracked']} competitors"
    )
    print(
        f"Monthly COGS: ${starter['monthly_cogs_usd']:.6f} "
        f"({starter['cogs_ratio']:.2%} of ${starter['list_price_usd']:.2f}; "
        f"cap {starter['cogs_cap_ratio']:.0%} = ${starter['cogs_cap_usd']:.2f})"
    )
    print(f"Gate: {'PASS' if starter['gate_passed'] else 'FAIL'}")
    print(f"AC#2 unblocked: {results['ac2_unblocked']}")
    if starter["fail_reasons"]:
        for reason in starter["fail_reasons"]:
            print(f"  FAIL: {reason}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inbound Score AC#0 COGS harness")
    parser.add_argument(
        "--no-live",
        action="store_true",
        help="Never call provider APIs even if keys are present",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RESULTS_DIR,
        help="Directory for JSON/CSV (default: product/cogs_spike/results)",
    )
    args = parser.parse_args(argv)
    results = build_results(live_probes=not args.no_live)
    json_path, csv_path = write_outputs(results, args.output_dir)
    print_summary(results)
    print()
    print(f"Wrote {json_path}")
    print(f"Wrote {csv_path}")
    return 0 if results["starter"]["gate_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
