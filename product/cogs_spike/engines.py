"""Locked engine set for Inbound Score free audit + Starter (AC#0).

AC#2 MUST use exactly these engines (provider + model/API). Do not add,
swap, or silently substitute models without a new COGS gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class EngineSpec:
    """One allowed visibility engine and its public list-price table."""

    engine_id: str
    provider: str
    model: str
    api: str
    endpoint: str
    input_usd_per_1m: float
    output_usd_per_1m: float
    request_fee_usd: float
    env_keys: tuple[str, ...]
    why: str
    tradeoff: str
    pricing_source: str
    pricing_as_of: str
    citation_native: bool


# Public list prices recorded 2026-09-13. Re-verify before raising Starter limits.
ALLOWED_ENGINES: tuple[EngineSpec, ...] = (
    EngineSpec(
        engine_id="openai:gpt-4.1-nano",
        provider="OpenAI",
        model="gpt-4.1-nano",
        api="Chat Completions (no web_search tool)",
        endpoint="https://api.openai.com/v1/chat/completions",
        input_usd_per_1m=0.10,
        output_usd_per_1m=0.40,
        request_fee_usd=0.0,
        env_keys=("OPENAI_API_KEY",),
        why=(
            "ChatGPT-class visibility is the question buyers ask first "
            "('does AI recommend us?'). gpt-4.1-nano is the cheapest official "
            "OpenAI chat model with a published list price, so we can cover "
            "20 prompts without web-search fees."
        ),
        tradeoff=(
            "API answers are not identical to the ChatGPT consumer UI. "
            "OpenAI web_search is $10 / 1k calls and is rejected for MVP COGS."
        ),
        pricing_source="https://developers.openai.com/api/docs/models/gpt-4.1-nano",
        pricing_as_of="2026-09-13",
        citation_native=False,
    ),
    EngineSpec(
        engine_id="google:gemini-2.5-flash-lite",
        provider="Google",
        model="gemini-2.5-flash-lite",
        api="Gemini Developer API generateContent (no search grounding)",
        endpoint="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent",
        input_usd_per_1m=0.10,
        output_usd_per_1m=0.40,
        request_fee_usd=0.0,
        env_keys=("GEMINI_API_KEY", "GOOGLE_API_KEY"),
        why=(
            "Gemini is the second buyer-relevant answer engine after ChatGPT. "
            "Flash-Lite is Google's cheapest current Gemini list price and is "
            "reliable enough for yes/no mention + vendor-list extraction."
        ),
        tradeoff=(
            "Grounding with Google Search is $35 / 1k prompts after a free "
            "quota. Paid COGS must not assume that quota, so MVP does not "
            "enable grounding. Mentions are model-knowledge, not live SERP."
        ),
        pricing_source="https://ai.google.dev/gemini-api/docs/pricing",
        pricing_as_of="2026-09-13",
        citation_native=False,
    ),
    EngineSpec(
        engine_id="perplexity:perplexity/sonar+web_search",
        provider="Perplexity",
        model="perplexity/sonar",
        api="Agent API responses.create with tools=[{type: web_search}]",
        endpoint="https://api.perplexity.ai/v1/agent",
        input_usd_per_1m=0.25,
        output_usd_per_1m=2.50,
        request_fee_usd=0.0025,  # one web_search invocation
        env_keys=("PERPLEXITY_API_KEY",),
        why=(
            "Only citation-native engine in the set: Agent API returns "
            "search_results URLs. Required for GEO 'who cites us' without "
            "inventing sources. Successor to Sonar Chat Completions, which "
            "retires 2026-09-27 — lock the Agent API now so AC#2 does not "
            "ship a dying endpoint."
        ),
        tradeoff=(
            "Request fee dominates unit cost (~$0.0025/call vs <<$0.001 tokens). "
            "Do not use Agent API presets (fast/low/…) — those can resolve to "
            "pricier third-party models. Do not add fetch_url."
        ),
        pricing_source=(
            "https://docs.perplexity.ai/docs/agent-api/models ; "
            "https://docs.perplexity.ai/docs/getting-started/pricing"
        ),
        pricing_as_of="2026-09-13",
        citation_native=True,
    ),
)


def get_engine(engine_id: str) -> EngineSpec:
    for engine in ALLOWED_ENGINES:
        if engine.engine_id == engine_id:
            return engine
    raise KeyError(f"Unknown engine_id: {engine_id}")


def engine_by_id() -> Mapping[str, EngineSpec]:
    return {engine.engine_id: engine for engine in ALLOWED_ENGINES}
