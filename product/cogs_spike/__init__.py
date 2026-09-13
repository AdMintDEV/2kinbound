"""Inbound Score AC#0 COGS / engines spike.

Allowed engines named here are the only engines AC#2 (free audit) may call.
Shortlist + list prices start from research/04_AC0_ENGINE_LIST_PRICES.md.
"""

from .calculator import (
    COGS_CAP_RATIO,
    LIST_PRICE_USD,
    RECOMMENDED_STARTER,
    StarterLimits,
    brand_runs_per_month,
    call_cost_usd,
    evaluate_gate,
    monthly_cogs_usd,
    run_cost_usd,
)
from .engines import ALLOWED_ENGINES, CANDIDATE_ENGINES, EngineSpec
from .prompts import PILOT_PROMPTS, SYSTEM_PROMPT, render_prompt

__all__ = [
    "ALLOWED_ENGINES",
    "CANDIDATE_ENGINES",
    "COGS_CAP_RATIO",
    "EngineSpec",
    "LIST_PRICE_USD",
    "PILOT_PROMPTS",
    "RECOMMENDED_STARTER",
    "SYSTEM_PROMPT",
    "StarterLimits",
    "brand_runs_per_month",
    "call_cost_usd",
    "evaluate_gate",
    "monthly_cogs_usd",
    "render_prompt",
    "run_cost_usd",
]
