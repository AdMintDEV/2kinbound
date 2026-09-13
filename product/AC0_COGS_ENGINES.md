# AC#0 — COGS / engines spike (GATE)

**Status:** **AC#0a PASS** (Reviewer `reviews/REVIEW_2026-09-13_AC0_PR1.md`) · **AC#0b TODO**  
**Date:** 2026-09-13  
**Product:** Inbound Score — free one-shot AI-visibility / GEO audit → paid Starter  
**ICP:** B2B SaaS companies with fewer than 50 employees  
**Starting shortlist + list prices:** `research/04_AC0_ENGINE_LIST_PRICES.md` (Research, FACT only)  
**Harness output:** `product/cogs_spike/results/ac0_pilot_results.json`

This file **names the only engines AC#2 code may use**. List prices from Research are **not** measured $/run.

| Gate | Meaning | Status | Unlocks |
|------|---------|--------|---------|
| **AC#0a** | Labeled ESTIMATE + ≤3 frozen engines + Starter ESTIMATE COGS &lt;30% of $29 | **PASS** | AC#1 landing; **implement** AC#2 **code** on the frozen IDs |
| **AC#0b** | Measured $/run (`usage` / invoice / approved `--live`) | **TODO** | **LAUNCH**; **live free-audit traffic**; MEASURED COGS claims |

AC#2 is **not** fully unblocked. Code may be written. Production / public engine spend waits on AC#0b.

## Final allowed engines (exactly 2 of the ≤3 shortlist)

| # | Engine ID | Provider + model / API | Why locked |
|---|-----------|------------------------|------------|
| 1 | **`openai-web-search`** | OpenAI **`gpt-4o-mini`** via Responses API + **`web_search`** | Research #1. Official API; citations via search. Model pinned because OpenAI documents the **8,000 search-content token** block for `gpt-4o-mini` / `gpt-4.1-mini`. |
| 2 | **`perplexity-sonar`** | Perplexity **`sonar`**, `search_context_size=low` | Research #2. Grounded answers + citations. Docs sample ~$0.00542/call (mostly the $0.005 low-context fee). |

AC#2 must call these IDs only. Do not scrape ChatGPT / Claude / Gemini UIs.

### Shortlist #3 — evaluated and dropped

| Engine ID | How we’d call it | Decision |
|-----------|------------------|----------|
| `perplexity-agent-web` | Perplexity Agent API + `web_search` ($0.0025/call + tokens) | **Dropped.** Redundant citations with Sonar. Adding it makes **24 brand-runs/mo × 3 engines = $9.67 ESTIMATE ≥ $8.70 cap**. Research: “prefer drop if COGS tight.” |

### Why not other engines

| Rejected | Why |
|----------|-----|
| Gemini consumer UI / unofficial scrape | Research forbid; ToS + unmeasurable |
| OpenAI without `web_search` | Cheaper, but fails the citation requirement the shortlist was built for |
| `gpt-5.6-luna` or unpinned “newest” models | 8k search-content block is **not** documented for them — token math would be hand-wavy |
| Sonar Pro / medium or high context | $0.008–$0.012 request fee; not needed for 20 short visibility probes |
| Groq / open weights | Not on the shortlist; zero GEO buyer relevance |

**Sonar sunset:** Perplexity Sonar Chat Completions retires **2026-09-27**. AC#2 may migrate to Agent API `perplexity/sonar` + `web_search` **only if** measured cost stays ≤ this Sonar-low table. That is a transport change, not a new engine ID, and still requires a harness re-run.

## Pilot design

A **run** = **one brand URL** × **20 prompts** × **the 2 locked engines** (40 visibility calls) + **one** `gpt-4o-mini` scoring roll-up (not a visibility engine).

Each tracked **competitor** is an extra run of the same 20×2 set.

- Prompts: B2B SaaS GEO templates in `product/cogs_spike/prompts.py`.
- Fixture brand `Northwind Analytics` / `https://www.example.com` is **token shape only**. No citation rows. No invented sources.
- **No API keys** in this environment. Harness dry-ran the Research list-price table. `--live` is opt-in because OpenAI `web_search` costs **$0.01/call** (not a free-tier probe). Human approval still required before meaningful spend.

```bash
PYTHONPATH=product python -m cogs_spike --no-live
```

## $/run — ESTIMATE (not measured)

**Do not treat this as measured.** There is no provider `usage` object and no invoice export for the 20-prompt set.

| Label | Meaning |
|-------|---------|
| **FACT** | Vendor list price copied from `research/04_AC0_ENGINE_LIST_PRICES.md` (fetched 2026-09-13) |
| **ESTIMATE qty** | Token counts from 4 chars ≈ 1 token on the real 20-prompt strings, plus a 280-token output budget |
| **ESTIMATE $/run** | FACT rates × ESTIMATE quantities + FACT per-call fees |

Recorded 2026-09-13 by the harness (`planned_mean_input_tokens` = **199**):

### `openai-web-search` — one call

| Component | Qty | Rate | $ | Basis |
|-----------|-----|------|---|-------|
| `web_search` tool | 1 | $10.00 / 1k = **$0.01** | **$0.010000** | FACT list price |
| Search-content tokens | 8,000 | $0.15 / 1M | **$0.001200** | FACT 8k block × FACT `gpt-4o-mini` input |
| Prompt tokens | 199 | $0.15 / 1M | **$0.000030** | ESTIMATE qty × FACT rate |
| Output tokens | 280 | $0.60 / 1M | **$0.000168** | ESTIMATE qty × FACT rate |
| **Call** | | | **$0.011398** | |
| **× 20 prompts** | | | **$0.227957** | |

### `perplexity-sonar` (low) — one call

| Component | Qty | Rate | $ | Basis |
|-----------|-----|------|---|-------|
| Low-context request fee | 1 | $5 / 1k = **$0.005** | **$0.005000** | FACT list price |
| Prompt tokens | 199 | $1 / 1M | **$0.000199** | ESTIMATE qty × FACT rate |
| Output tokens | 280 | $1 / 1M | **$0.000280** | ESTIMATE qty × FACT rate |
| **Call** | | | **$0.005479** | (docs sample $0.00542 for 9/402 tokens) |
| **× 20 prompts** | | | **$0.109580** | |

### Scoring roll-up (not an engine)

`gpt-4o-mini`, no web_search: 1616 in × $0.15/1M + 400 out × $0.60/1M = **$0.000482 ESTIMATE**.

### Totals

```
$/run mean (ESTIMATE) = $0.227957 + $0.109580 + $0.000482 = $0.338019
$/run p95 (ESTIMATE)  = Sonar medium fee $0.008 + 1.5× output tokens = $0.402499
```

p95 is also **ESTIMATE**, not a measured percentile. Fees dominate: $0.01×20 + $0.005×20 = **$0.30 of $0.338** is FACT per-call charges. Token-quantity error cannot hide that.

## Starter limits (estimated COGS < 30% of $29)

Research note: daily 20×2 scans cannot fit (~$0.007/call budget). Starter is **weekly + limited on-demand**.

| Limit | Value |
|-------|-------|
| List price | **$29/mo** ($19 floor not used) |
| On-demand audits | **2 / month** |
| Scheduled rechecks | **4 / month** (weekly) |
| Competitors tracked | **2** |
| Brand-runs / month | **(1+2) × (2+4) = 18** |
| Monthly COGS mean ESTIMATE | **$6.08** (18 × $0.338019) |
| Monthly COGS p95 ESTIMATE | **$7.24** (18 × $0.402499) |
| COGS / $29 | **20.98%** mean / **25.0%** p95 |
| Cap | 30% = **$8.70** |
| Gate | **PASS** |

Why not 4 on-demand + 4 weekly + 2 competitors (24 runs)?  
24 × $0.338 = **$8.11** (28%) on the mean — no room if Sonar is medium or a call retries. 24 × 3-engine ESTIMATE = **$9.67 FAIL**.

Free audit (marketing): **3 / IP / day**, **same 2 engines**, ~$0.34 ESTIMATE each. Abuse control is the rate limit.

## FAIL criteria

1. Estimated or measured monthly COGS at intended Starter limits **≥ 30% of $29 ($8.70)**.
2. $19 floor **and** minimum-viable limits (2+2+1 competitor) still cannot keep COGS **< 30% of $19 ($5.70)**.
3. Locked set has no citation-native engine.
4. Later **measured** $/run is **>2×** this estimate **and** breaks the cap — new AC#0 revision required.
5. **List prices in `research/04` are not measured $/run.**
6. No scrapers, no invented citations, no skipped prompts to “make the math work.”

This spike: **none triggered.**

## AC#2: code vs live

**Code (AC#0a — allowed now):** implement the free-audit path against **exactly** `openai-web-search` and `perplexity-sonar`. Rate-limit. Persist timestamps. Store only sources an API returned. Never invent citations.

**Live / LAUNCH (AC#0b — still closed):** do **not** send public free-audit traffic to those APIs, do not claim MEASURED COGS, and do not treat `--live` as approved until human-approved keys exist and a usage/invoice ledger replaces this ESTIMATE.

Default runtime is a **safe stub** (no HTTP to OpenAI/Perplexity). Live calls require all of:

1. `INBOUND_SCORE_LIVE=1` (explicit opt-in)
2. `OPENAI_API_KEY` and `PERPLEXITY_API_KEY`
3. `INBOUND_SCORE_AC0B=1` (AC#0b cleared)

Missing any of those → stub, empty citation list, no spend.

Do **not** run `--live` or set those env vars without human-approved keys. This environment has not done so.

## Harness + tests

| Path | Role |
|------|------|
| `research/04_AC0_ENGINE_LIST_PRICES.md` | Starting shortlist + FACT list prices |
| `product/cogs_spike/engines.py` | Candidates, lock, drop |
| `product/cogs_spike/calculator.py` | Line-item ledger, $/run, gate |
| `product/cogs_spike/harness.py` | Dry-run / opt-in `--live` |
| `product/cogs_spike/results/` | JSON + CSV |
| `tests/test_cogs_spike.py` | Math + ledger + gate (no network) |
