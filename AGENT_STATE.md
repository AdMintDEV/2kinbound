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

SELECT **ACCEPTED** for Inbound Score. Next: Builder **T3** starts with **AC#0 COGS/engines spike**, then smallest shippable paid path. Parallel: Research may propose faster $0.01 experiments if GEO COGS fails validation.

## Completed work

- Shared memory seeded; Forge + mission histories merged on `main`
- DISCOVER/VALIDATE v1.1 + scorecard
- SELECT wedge + ordered MVP AC (AC#0 gates free audit engines)
- Reviewer FAIL r1/r2 addressed (Forge scope, AC gate, refs)
- Forge toolkit: ingest/score/store/CLI/dashboard + 20 tests (library only)

## Active work

- T3 BUILD Inbound Score (Builder) — unlocked after SELECT ACCEPTED
- Shared profit tracking (`REVENUE.md`) initialized at $0

## Remaining work

- AC#0 COGS pilot (list-price inputs: `research/04_AC0_ENGINE_LIST_PRICES.md`) → AC#1–6 MVP → TEST → LAUNCH → first paid conversion
- Distribution that gets real buyers
- Measure net profit; iterate or kill by SELECT kill criteria
- T8: faster $0.01 paths documented in `OPPORTUNITIES.md` (F1–F4); activate only if GEO blocked

## Known failures

- Prior remote/local divergence (Forge vs mission) — resolved by merge
- Prior false “mission complete” on Forge-only state — corrected

## Blockers

- None for starting AC#0. Human approval still required before meaningful spend (domains, paid APIs at scale, ads).

## Next action

**Builder:** run AC#0 COGS/engines spike and write results under `product/`; then land smallest testable surface toward free audit + Stripe test mode.  
**Research:** keep Plan B / faster $0.01 options updated in `OPPORTUNITIES.md`.  
**Reviewer:** PASS mission only when `REVENUE.md` shows real net profit &gt; 0.
