# AGENT_STATE

**Updated:** 2026-09-13  
**Authority:** Team shared state for the autonomous profit mission. Repo files beat chat.

## Current mission

Build, launch, operate, and improve a legitimate internet business that produces **net profit** (revenue − attributable costs).  
First milestone: **$0.01 legitimate net profit**. Then scale toward $100 → $500 → $1,000 → $2,000/mo with rising automation.  
Code, MVP, and launch alone do **not** complete the mission.

## Current product

**Inbound Score** (selected experiment): free AI-visibility / GEO audit → paid monitoring for **B2B SaaS &lt;50 employees**.  
Also in-repo: **Forge** (`src/forge/`) — internal research-scoring toolkit (complete as a library; not the profit product).

## Current experiment

SELECT **ACCEPTED**. **AC#0 DONE** from Research shortlist `research/04_AC0_ENGINE_LIST_PRICES.md`. T3 remains IN_PROGRESS (AC#1 next). List prices were **not** treated as measured $/run.

## Completed work

- Shared memory seeded; Forge + mission histories merged on `main`
- DISCOVER/VALIDATE v1.1 + scorecard
- SELECT wedge + ordered MVP AC (AC#0 gates free audit engines)
- Reviewer FAIL r1/r2 addressed (Forge scope, AC gate, refs)
- Forge toolkit: ingest/score/store/CLI/dashboard + 20 tests (library only)
- Research AC#0 list-price shortlist + T8 F1–F4 paths
- **AC#0:** locked `openai-web-search` + `perplexity-sonar`; dropped `perplexity-agent-web`. ESTIMATE $/run **$0.338019** (p95 ESTIMATE $0.402499). Starter 2 on-demand + 4 weekly + 2 competitors → COGS **20.98%** of $29. See `product/AC0_COGS_ENGINES.md`.

## Active work

- T3 BUILD Inbound Score (Builder) — **IN_PROGRESS**; AC#0 done, AC#1 (landing) is next
- Shared profit tracking (`REVENUE.md`) remains $0 — do not invent revenue

## Remaining work

- AC#1–6 MVP (landing, free audit on the **locked engine set**, Stripe, persist, tests, no spam) → TEST → LAUNCH → first paid conversion
- Distribution that gets real buyers
- Measure net profit; iterate or kill by SELECT kill criteria
- T8: faster $0.01 paths documented in `OPPORTUNITIES.md` (F1–F4); activate only if GEO blocked

## Known failures

- Prior remote/local divergence (Forge vs mission) — resolved by merge
- Prior false “mission complete” on Forge-only state — corrected
- AC#0 $/run is **ESTIMATE** (no API keys / no usage export). Re-run harness when keys exist; do not relabel MEASURED until then.

## Blockers

- None for starting AC#1. Human approval still required before meaningful spend (domains, paid APIs at scale, ads).
- AC#2 must use exactly: `openai-web-search`, `perplexity-sonar`.

## Next action

**Builder:** AC#1 public landing page (value prop, ICP, $29, CTA). AC#2 uses only the AC#0 engine IDs.  
**Research:** keep Plan B / faster $0.01 options updated in `OPPORTUNITIES.md`.  
**Reviewer:** PASS mission only when `REVENUE.md` shows real net profit &gt; 0.
