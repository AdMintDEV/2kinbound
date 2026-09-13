"""Engine shortlist and locked set for Inbound Score (AC#0).

Starting shortlist + list prices: `research/04_AC0_ENGINE_LIST_PRICES.md`
(Research, 2026-09-13). Those prices are FACT list prices, NOT measured $/run.

AC#2 MUST use exactly ALLOWED_ENGINES. Do not add, swap, or scrape consumer UIs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


RESEARCH_PRICE_DOC = "research/04_AC0_ENGINE_LIST_PRICES.md"
PRICING_AS_OF = "2026-09-13"


@dataclass(frozen=True)
class EngineSpec:
    """One visibility engine and its published list-price table."""

    engine_id: str
    provider: str
    model: str
    api: str
    endpoint: str
    input_usd_per_1m: float
    output_usd_per_1m: float
    request_fee_usd: float
    extra_input_tokens: int
    extra_input_reason: str
    env_keys: tuple[str, ...]
    why: str
    tradeoff: str
    pricing_source: str
    pricing_as_of: str
    citation_native: bool
    research_role: str  # shortlist | locked | dropped


def _openai_web_search() -> EngineSpec:
    return EngineSpec(
        engine_id="openai-web-search",
        provider="OpenAI",
        model="gpt-4o-mini",
        api="Responses API + web_search tool",
        endpoint="https://api.openai.com/v1/responses",
        input_usd_per_1m=0.15,
        output_usd_per_1m=0.60,
        request_fee_usd=0.01,  # $10.00 / 1k web_search calls
        extra_input_tokens=8_000,
        extra_input_reason=(
            "FACT from OpenAI pricing: gpt-4o-mini / gpt-4.1-mini non-preview "
            "web_search bills a fixed 8,000 search-content input tokens per call"
        ),
        env_keys=("OPENAI_API_KEY",),
        why=(
            "Research shortlist #1. Official API with citations via web_search. "
            "Pinned gpt-4o-mini because that is the model the 8k search-content "
            "block is documented against — token math is then sourced, not guessed."
        ),
        tradeoff=(
            "Web search is $0.01/call before tokens. 20 prompts ≈ $0.20+ just "
            "for OpenAI. Do not use gpt-5.6-luna / unmarked models: the 8k block "
            "is not documented for them. API+search ≠ ChatGPT consumer UI."
        ),
        pricing_source="https://developers.openai.com/api/docs/pricing",
        pricing_as_of=PRICING_AS_OF,
        citation_native=True,
        research_role="locked",
    )


def _perplexity_sonar() -> EngineSpec:
    return EngineSpec(
        engine_id="perplexity-sonar",
        provider="Perplexity",
        model="sonar",
        api="Sonar Chat Completions, search_context_size=low",
        endpoint="https://api.perplexity.ai/chat/completions",
        input_usd_per_1m=1.0,
        output_usd_per_1m=1.0,
        request_fee_usd=0.005,  # $5 / 1k low-context requests
        extra_input_tokens=0,
        extra_input_reason="",
        env_keys=("PERPLEXITY_API_KEY",),
        why=(
            "Research shortlist #2. Grounded answers + citations. Request fee "
            "($0.005 low) dominates; docs sample ~$0.00542 for a small call. "
            "Second buyer-relevant engine after ChatGPT-class search."
        ),
        tradeoff=(
            "Sonar Chat Completions retires 2026-09-27. AC#2 may call the "
            "Agent API successor (`perplexity/sonar` + web_search) only if "
            "cost is ≤ this Sonar-low table. Do not silently upgrade to "
            "Sonar Pro / medium/high context."
        ),
        pricing_source="https://docs.perplexity.ai/docs/getting-started/pricing",
        pricing_as_of=PRICING_AS_OF,
        citation_native=True,
        research_role="locked",
    )


def _perplexity_agent_web() -> EngineSpec:
    return EngineSpec(
        engine_id="perplexity-agent-web",
        provider="Perplexity",
        model="perplexity/sonar",
        api="Agent API + web_search tool",
        endpoint="https://api.perplexity.ai/v1/agent",
        input_usd_per_1m=0.25,
        output_usd_per_1m=2.50,
        request_fee_usd=0.0025,
        extra_input_tokens=0,
        extra_input_reason="",
        env_keys=("PERPLEXITY_API_KEY",),
        why=(
            "Research shortlist #3 (optional). Same vendor as Sonar; extra "
            "citation path via Agent API web_search ($0.0025/invocation)."
        ),
        tradeoff=(
            "Dropped: redundant with perplexity-sonar citations, and "
            "20 extra calls/run push 4+4+2 Starter limits over the 30% cap. "
            "Research: 'prefer drop if COGS tight'."
        ),
        pricing_source=(
            "https://docs.perplexity.ai/docs/getting-started/pricing ; "
            "https://docs.perplexity.ai/docs/agent-api/models"
        ),
        pricing_as_of=PRICING_AS_OF,
        citation_native=True,
        research_role="dropped",
    )


# Research ≤3 candidates, in shortlist order.
CANDIDATE_ENGINES: tuple[EngineSpec, ...] = (
    _openai_web_search(),
    _perplexity_sonar(),
    _perplexity_agent_web(),
)

# Final freeze for free audit + Starter. #3 dropped (COGS).
ALLOWED_ENGINES: tuple[EngineSpec, ...] = tuple(
    e for e in CANDIDATE_ENGINES if e.research_role == "locked"
)
DROPPED_ENGINES: tuple[EngineSpec, ...] = tuple(
    e for e in CANDIDATE_ENGINES if e.research_role == "dropped"
)

# Not a visibility engine — cheap roll-up of the 20×N JSON snippets.
SCORING_ENGINE = EngineSpec(
    engine_id="openai-scoring-roll-up",
    provider="OpenAI",
    model="gpt-4o-mini",
    api="Chat Completions (no web_search)",
    endpoint="https://api.openai.com/v1/chat/completions",
    input_usd_per_1m=0.15,
    output_usd_per_1m=0.60,
    request_fee_usd=0.0,
    extra_input_tokens=0,
    extra_input_reason="",
    env_keys=("OPENAI_API_KEY",),
    why="Internal scoring only. Not part of the AC#2 visibility engine set.",
    tradeoff="Must never be advertised as a third/fourth GEO engine.",
    pricing_source="https://developers.openai.com/api/docs/models/gpt-4o-mini",
    pricing_as_of=PRICING_AS_OF,
    citation_native=False,
    research_role="scoring",
)


def get_engine(engine_id: str) -> EngineSpec:
    for engine in (*CANDIDATE_ENGINES, SCORING_ENGINE):
        if engine.engine_id == engine_id:
            return engine
    raise KeyError(f"Unknown engine_id: {engine_id}")


def engine_by_id() -> Mapping[str, EngineSpec]:
    return {engine.engine_id: engine for engine in CANDIDATE_ENGINES}
