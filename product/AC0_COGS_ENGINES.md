# AC#0 — COGS / engines spike (GATE)

**Status:** DONE (dry-run ESTIMATE; live spend = $0)  
**Date:** 2026-09-13  
**Product:** Inbound Score — free one-shot AI-visibility / GEO audit → paid Starter  
**ICP:** B2B SaaS companies with fewer than 50 employees  
**Source of numbers:** `product/cogs_spike/` harness + `product/cogs_spike/results/ac0_pilot_results.json`

This file **names the only engines AC#2 may use**. Do not ship the free audit until that set is wired exactly.

## Allowed engines (exactly 3)

| # | Provider | Model / API | Endpoint | List price (2026-09-13) | Role |
|---|----------|-------------|----------|-------------------------|------|
| 1 | **OpenAI** | `gpt-4.1-nano` via Chat Completions (**no** `web_search`) | `https://api.openai.com/v1/chat/completions` | $0.10 / 1M in · $0.40 / 1M out | ChatGPT-class mention / shortlist |
| 2 | **Google** | `gemini-2.5-flash-lite` via Gemini Developer API (**no** search grounding) | `…/models/gemini-2.5-flash-lite:generateContent` | $0.10 / 1M in · $0.40 / 1M out | Gemini-class mention / shortlist |
| 3 | **Perplexity** | `perplexity/sonar` via **Agent API** + `tools=[{type: web_search}]` | `https://api.perplexity.ai/v1/agent` | $0.25 / 1M in · $2.50 / 1M out + **$0.0025 / web_search** | Citation-native engine |

Canonical IDs (do not rename without a new AC#0 revision):

1. `openai:gpt-4.1-nano`
2. `google:gemini-2.5-flash-lite`
3. `perplexity:perplexity/sonar+web_search`

### Why each

- **OpenAI `gpt-4.1-nano`:** Buyers ask “does ChatGPT recommend us?” This is the cheapest official OpenAI chat model with a published list price, so 20 prompts stay far under a cent. Official API only (ToS).
- **Google `gemini-2.5-flash-lite`:** Second buyer-relevant answer engine. Cheapest current Gemini list price; reliable enough for yes/no mention + vendor-list extraction.
- **Perplexity Agent API `perplexity/sonar` + `web_search`:** Only citation-native engine. Returns `search_results` URLs so we do not invent citations. **Must use Agent API**, not legacy Sonar Chat Completions (`POST /chat/completions` / `model=sonar`), which retires **2026-09-27**.

### Tradeoffs (accepted for MVP)

| Rejected / deferred | Why not in the locked set |
|---------------------|---------------------------|
| OpenAI `web_search` | $10 / 1k calls → $0.01 × 20 = $0.20 just for ChatGPT search. Breaks cheap 20-prompt design. |
| Gemini Grounding with Google Search | $35 / 1k after free quota. Paid COGS must not assume the free quota. |
| Perplexity Agent API **presets** (`fast` / `low` / …) | Presets can resolve to third-party models (e.g. `openai/gpt-5.4-mini`) and raise $/call. Lock the `perplexity/sonar` slug + one `web_search`. |
| Perplexity `fetch_url` | Extra $0.0005+ / call; not needed to record `search_results`. |
| Anthropic Haiku / Claude | Higher token price; less “does ChatGPT/Gemini/Perplexity mention us?” buyer relevance than the three above. |
| Groq / open weights via a host | Cheapest tokens, **zero** GEO buyer relevance (nobody asks “does Llama recommend us?”). |
| Consumer-UI scrape of chatgpt.com / perplexity.ai | ToS + ban risk. Official APIs only. |

API answers ≠ consumer ChatGPT/Gemini UIs. The free audit must say that. Mentions on OpenAI/Gemini are model-knowledge probes; only Perplexity is live-web + citations.

## Pilot design

A **run** = **one brand URL** × **20 prompts** × **these 3 engines** (60 visibility calls) + **one** `gpt-4.1-nano` scoring roll-up (not a fourth visibility engine).

Each tracked **competitor** is an extra run of the same 20×3 set.

- Prompt set: B2B SaaS GEO / visibility templates in `product/cogs_spike/prompts.py` (category shortlists, “tools like {brand}”, vs-competitor, cite-URL, five-name lists).
- Fixture brand is `Northwind Analytics` / `https://www.example.com` — **token shape only**. This spike does **not** produce citation rows and does **not** claim a real audit.
- 48h / near-zero spend: **no provider API keys** were present in this environment. The harness dry-ran the pricing table. Optional 1-call live probes run only when `OPENAI_API_KEY` / `GEMINI_API_KEY` or `GOOGLE_API_KEY` / `PERPLEXITY_API_KEY` exist (`--no-live` to force dry-run).
- Human approval is still required before meaningful paid-API spend.

```bash
PYTHONPATH=product python -m cogs_spike --no-live
# or
PYTHONPATH=product python product/cogs_spike/harness.py --no-live
```

## $/run — ESTIMATE (not measured)

**Cost basis: ESTIMATE.** Public list prices × estimated tokens (4 characters ≈ 1 token). No billed usage was returned because no keys were set. Do not treat these figures as measured invoices.

Recorded 2026-09-13 by the harness:

| Component | Tokens in / out (plan) | $/call | ×20 | Source |
|-----------|------------------------|--------|-----|--------|
| OpenAI `gpt-4.1-nano` | 199 / 280 | $0.000132 | **$0.002638** | [OpenAI gpt-4.1-nano](https://developers.openai.com/api/docs/models/gpt-4.1-nano) |
| Google `gemini-2.5-flash-lite` | 199 / 280 | $0.000132 | **$0.002638** | [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| Perplexity `perplexity/sonar` + 1× `web_search` | 199 / 280 | $0.003250 | **$0.064995** | [Agent models](https://docs.perplexity.ai/docs/agent-api/models) · [Pricing](https://docs.perplexity.ai/docs/getting-started/pricing) |
| Scoring roll-up (OpenAI, 1×) | 1616 / 400 | $0.000322 | **$0.000322** | same OpenAI table |

**$/run = $0.070593 (ESTIMATE)**

Math:

```
OpenAI/Gemini call = (199 × 0.10 + 280 × 0.40) / 1e6 = $0.0001319
Perplexity call    = (199 × 0.25 + 280 × 2.50) / 1e6 + $0.0025 = $0.00324975
Run                = 20 × ($0.0001319 + $0.0001319 + $0.00324975) + $0.0003216
                   = $0.0705926
```

Perplexity’s **$0.0025 web_search fee** is ~92% of run cost. Token error on OpenAI/Gemini barely moves the total.

### Stress (still ESTIMATE)

| Scenario | $/run | 24 brand-runs / mo | vs $29 |
|----------|-------|--------------------|--------|
| Baseline (above) | $0.071 | $1.69 | **5.8%** |
| 3× tokens | ~$0.11 | ~$2.7 | ~9% |
| 2× `web_search` per Perplexity call | ~$0.12 | ~$2.9 | ~10% |
| 2× tokens **and** 2× search | ~$0.16 | ~$3.8 | ~13% |

Headroom to the 30% cap ($8.70) is large. **Stay at $29/mo. The $19 floor is not needed.**

## Starter limits (keep estimated COGS < 30% of $29)

| Limit | Value | Notes |
|-------|-------|-------|
| List price | **$29/mo** | Floor $19 not invoked |
| On-demand audits | **4 / month** | Full 20×3 run each |
| Scheduled rechecks | **4 / month** | Weekly; same run shape |
| Competitors tracked | **2** | Each competitor = +1 run per audit/recheck |
| Brand-runs / month | **(1+2) × (4+4) = 24** | |
| Estimated monthly COGS | **$1.69** | 24 × $0.070593 |
| COGS / list | **5.84%** | Cap = 30% = $8.70 |
| Gate | **PASS** | |

Free audit (marketing, not Starter COGS): **3 / IP / day**, **same 3 engines**, same 20-prompt run. ESTIMATE ~$0.07 per free audit. Abuse control is the rate limit, not a cheaper engine set.

AC#3 (dashboard / weekly email) must enforce these numeric caps. Caching identical `(brand_url, prompt, engine)` within a recheck window is allowed and only improves margin.

## FAIL criteria (do not ship AC#2 if any trigger)

1. Estimated or measured monthly COGS at the intended Starter limits is **≥ 30% of $29.00 ($8.70)**.
2. Dropping to the **$19 floor** **and** minimum-viable limits (2 on-demand + 2 weekly rechecks + 1 competitor) still cannot keep COGS **< 30% of $19.00 ($5.70)**.
3. The locked set cannot include a **citation-native** engine under the cap (that engine is Perplexity Agent API `perplexity/sonar` + `web_search`).
4. A later live measurement is **>2×** this estimate **and** the inflated $/run breaks the 30% cap — re-run the harness; tighten limits or drop an engine **only** via a new AC#0 revision.
5. Do not “fix” a FAIL by inventing citations, skipping prompts, or swapping in unofficial scrapers / consumer-UI automation.

This spike: **none of the FAIL criteria triggered.**

## AC#2 unblock

**Yes — AC#2 is unblocked** on engines + unit COGS.

Wire the free audit to **exactly** the three IDs above. Persist provider response timestamps; store only sources the engine returned; never invent citations.

## Harness + tests

| Path | Role |
|------|------|
| `product/cogs_spike/engines.py` | Locked engine table + list prices |
| `product/cogs_spike/prompts.py` | 20-prompt set |
| `product/cogs_spike/calculator.py` | $/call, $/run, Starter limit math, gate |
| `product/cogs_spike/harness.py` | Dry-run / optional live probe; writes results |
| `product/cogs_spike/results/ac0_pilot_results.json` | Machine-readable pilot record |
| `product/cogs_spike/results/ac0_pilot_results.csv` | Same, tabular |
| `tests/test_cogs_spike.py` | Math + gate + dry-run I/O (no network) |
