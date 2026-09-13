"""Deterministic COGS math for the AC#0 spike. No network I/O."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable, Sequence

from .engines import ALLOWED_ENGINES, EngineSpec
from .prompts import DEFAULT_BRAND, PILOT_PROMPTS, SYSTEM_PROMPT, BrandContext, brand_block, render_prompt

# OpenAI-published rule of thumb; used only when a provider does not return usage.
# All costs derived from this path MUST be labeled ESTIMATE.
CHARS_PER_TOKEN = 4.0

# Structured-answer budget (JSON keys + short snippet). Conservative for planning.
PLANNED_OUTPUT_TOKENS = 280

# One cheap OpenAI roll-up per brand-run (not a fourth visibility engine).
SCORING_ENGINE_ID = "openai:gpt-4.1-nano"
SCORING_OUTPUT_TOKENS = 400

LIST_PRICE_USD = 29.0
PRICE_FLOOR_USD = 19.0
COGS_CAP_RATIO = 0.30  # AC#0: estimated COGS < 30% of list

# Free audit (marketing). Same engine set. Not counted in Starter COGS.
FREE_AUDITS_PER_IP_PER_DAY = 3


@dataclass(frozen=True)
class StarterLimits:
    list_price_usd: float = LIST_PRICE_USD
    on_demand_audits_per_month: int = 4
    scheduled_rechecks_per_month: int = 4
    competitors_tracked: int = 2
    cogs_cap_ratio: float = COGS_CAP_RATIO


RECOMMENDED_STARTER = StarterLimits()

# Tightest still-useful Starter if list-price COGS fails (used by FAIL criteria).
MINIMUM_VIABLE_STARTER = StarterLimits(
    list_price_usd=PRICE_FLOOR_USD,
    on_demand_audits_per_month=2,
    scheduled_rechecks_per_month=2,
    competitors_tracked=1,
)


@dataclass(frozen=True)
class TokenUse:
    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class CallCost:
    engine_id: str
    tokens: TokenUse
    token_cost_usd: float
    request_fee_usd: float
    total_usd: float
    cost_basis: str  # ESTIMATE | MEASURED


@dataclass(frozen=True)
class GateResult:
    passed: bool
    cost_per_run_usd: float
    monthly_cogs_usd: float
    cogs_ratio: float
    cap_usd: float
    brand_runs_per_month: int
    limits: StarterLimits
    fail_reasons: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict:
        payload = asdict(self)
        return payload


def estimate_tokens(text: str) -> int:
    """Character/4 token estimate. ESTIMATE, not a billed tokenizer."""
    if not text:
        return 0
    return max(1, int((len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN))


def rendered_inputs(
    brand: BrandContext = DEFAULT_BRAND,
    prompts: Sequence[str] = PILOT_PROMPTS,
) -> list[str]:
    header = brand_block(brand)
    return [f"{header}\n{render_prompt(template, brand)}" for template in prompts]


def mean_input_tokens(
    brand: BrandContext = DEFAULT_BRAND,
    prompts: Sequence[str] = PILOT_PROMPTS,
    system_prompt: str = SYSTEM_PROMPT,
) -> int:
    bodies = rendered_inputs(brand, prompts)
    if not bodies:
        raise ValueError("prompt set must not be empty")
    totals = [estimate_tokens(system_prompt) + estimate_tokens(body) for body in bodies]
    return int(round(sum(totals) / len(totals)))


def call_cost_usd(
    engine: EngineSpec,
    tokens: TokenUse,
    *,
    cost_basis: str = "ESTIMATE",
) -> CallCost:
    if tokens.input_tokens < 0 or tokens.output_tokens < 0:
        raise ValueError("token counts must be >= 0")
    token_cost = (
        tokens.input_tokens * engine.input_usd_per_1m
        + tokens.output_tokens * engine.output_usd_per_1m
    ) / 1_000_000
    total = token_cost + engine.request_fee_usd
    return CallCost(
        engine_id=engine.engine_id,
        tokens=tokens,
        token_cost_usd=token_cost,
        request_fee_usd=engine.request_fee_usd,
        total_usd=total,
        cost_basis=cost_basis,
    )


def visibility_call_cost(
    engine: EngineSpec,
    *,
    input_tokens: int,
    output_tokens: int = PLANNED_OUTPUT_TOKENS,
    cost_basis: str = "ESTIMATE",
) -> CallCost:
    return call_cost_usd(
        engine,
        TokenUse(input_tokens=input_tokens, output_tokens=output_tokens),
        cost_basis=cost_basis,
    )


def scoring_input_tokens(prompt_count: int, snippet_tokens: int = 80) -> int:
    """Roll-up reads prompt_count short snippets plus a fixed instruction."""
    instruction = estimate_tokens(
        "Score mention rates. Input is JSON snippets. Return counts only."
    )
    return instruction + prompt_count * snippet_tokens


def scoring_call_cost(engines: Iterable[EngineSpec] = ALLOWED_ENGINES) -> CallCost:
    scoring = next(e for e in engines if e.engine_id == SCORING_ENGINE_ID)
    tokens = TokenUse(
        input_tokens=scoring_input_tokens(len(PILOT_PROMPTS)),
        output_tokens=SCORING_OUTPUT_TOKENS,
    )
    return call_cost_usd(scoring, tokens, cost_basis="ESTIMATE")


def run_cost_usd(
    *,
    engines: Sequence[EngineSpec] = ALLOWED_ENGINES,
    input_tokens: int | None = None,
    output_tokens: int = PLANNED_OUTPUT_TOKENS,
    prompt_count: int = 20,
    include_scoring: bool = True,
    measured_by_engine: dict[str, TokenUse] | None = None,
) -> tuple[float, list[CallCost], str]:
    """Cost of one brand-URL audit (prompt_count × each engine, plus scoring).

    A 'run' is one brand URL across the locked engine set. Competitors are
    extra runs, not extra engines.
    """
    if not 1 <= len(engines) <= 3:
        raise ValueError("AC#0 allows at most 3 engines")
    if prompt_count != 20:
        raise ValueError("AC#0 pilot is defined as 20 prompts")

    planned_in = input_tokens if input_tokens is not None else mean_input_tokens()
    per_call: list[CallCost] = []
    bases: list[str] = []
    for engine in engines:
        measured = (measured_by_engine or {}).get(engine.engine_id)
        if measured is not None:
            cost = call_cost_usd(engine, measured, cost_basis="MEASURED")
        else:
            cost = visibility_call_cost(
                engine, input_tokens=planned_in, output_tokens=output_tokens
            )
        per_call.append(cost)
        bases.append(cost.cost_basis)

    visibility_only = list(per_call)
    visibility_total = prompt_count * sum(c.total_usd for c in visibility_only)
    scoring = scoring_call_cost(engines) if include_scoring else None
    scoring_total = scoring.total_usd if scoring else 0.0
    if scoring:
        per_call.append(scoring)
        bases.append(scoring.cost_basis)

    vis_measured = bool(visibility_only) and all(
        c.cost_basis == "MEASURED" for c in visibility_only
    )
    vis_any_measured = any(c.cost_basis == "MEASURED" for c in visibility_only)
    if vis_measured and not include_scoring:
        basis = "MEASURED"
    elif vis_any_measured:
        basis = "MIXED"
    else:
        basis = "ESTIMATE"

    return visibility_total + scoring_total, per_call, basis


def brand_runs_per_month(limits: StarterLimits) -> int:
    brands = 1 + limits.competitors_tracked
    audits = limits.on_demand_audits_per_month + limits.scheduled_rechecks_per_month
    if brands < 1 or audits < 0:
        raise ValueError("invalid Starter limits")
    return brands * audits


def monthly_cogs_usd(cost_per_run: float, limits: StarterLimits) -> float:
    if cost_per_run < 0:
        raise ValueError("cost_per_run must be >= 0")
    return brand_runs_per_month(limits) * cost_per_run


def cogs_ratio(monthly_cogs: float, list_price: float) -> float:
    if list_price <= 0:
        raise ValueError("list_price must be > 0")
    return monthly_cogs / list_price


def cap_usd(list_price: float, ratio: float = COGS_CAP_RATIO) -> float:
    return list_price * ratio


def evaluate_gate(
    cost_per_run: float,
    limits: StarterLimits = RECOMMENDED_STARTER,
    *,
    floor_price: float = PRICE_FLOOR_USD,
    minimum: StarterLimits = MINIMUM_VIABLE_STARTER,
) -> GateResult:
    """PASS only if estimated monthly COGS is strictly < 30% of the list price."""
    monthly = monthly_cogs_usd(cost_per_run, limits)
    ratio = cogs_ratio(monthly, limits.list_price_usd)
    cap = cap_usd(limits.list_price_usd, limits.cogs_cap_ratio)
    reasons: list[str] = []
    if monthly >= cap:
        reasons.append(
            f"Monthly COGS ${monthly:.4f} is not < {limits.cogs_cap_ratio:.0%} of "
            f"${limits.list_price_usd:.2f} (cap ${cap:.4f})."
        )
        min_monthly = monthly_cogs_usd(cost_per_run, minimum)
        floor_cap = cap_usd(floor_price, COGS_CAP_RATIO)
        if min_monthly >= floor_cap:
            reasons.append(
                f"Even minimum-viable limits fail the ${floor_price:.2f} floor: "
                f"${min_monthly:.4f} >= ${floor_cap:.4f}."
            )
        else:
            reasons.append(
                f"Minimum-viable limits would pass at ${floor_price:.2f} "
                f"(${min_monthly:.4f} < ${floor_cap:.4f}) — human must approve "
                f"the floor before shipping AC#2."
            )
    return GateResult(
        passed=not reasons,
        cost_per_run_usd=cost_per_run,
        monthly_cogs_usd=monthly,
        cogs_ratio=ratio,
        cap_usd=cap,
        brand_runs_per_month=brand_runs_per_month(limits),
        limits=limits,
        fail_reasons=tuple(reasons),
    )


FAIL_CRITERIA: tuple[str, ...] = (
    "FAIL AC#0 / do not ship AC#2 if estimated or measured monthly COGS at the "
    "intended Starter limits is >= 30% of $29.00 ($8.70).",
    "FAIL if dropping to the $19 floor AND minimum-viable limits "
    "(2 on-demand audits + 2 weekly rechecks + 1 competitor) still cannot keep "
    "COGS < 30% of $19.00 ($5.70).",
    "FAIL if the locked set cannot include a citation-native engine under the cap "
    "(Perplexity Agent API perplexity/sonar + web_search is that engine).",
    "FAIL if a later live measurement is >2× this estimate and the inflated "
    "$/run breaks the 30% cap — re-run this harness and tighten limits or drop "
    "an engine only via a new AC#0 revision.",
    "Do not 'fix' a FAIL by inventing citations, skipping prompts, or swapping "
    "in unofficial scrapers / consumer-UI automation.",
)
