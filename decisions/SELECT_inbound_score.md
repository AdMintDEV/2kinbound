# SELECT: Inbound Score = AI visibility / GEO monitoring

**Status:** ACCEPTED  
**Date:** 2026-09-13  
**Evidence:** `research/02_DISCOVER_VALIDATE.md` v1.1  
**Remote:** mission + Forge on `main` (`b4b67ab` — see also `01_STATE.md`)

## Decision

Build **Inbound Score**: free one-shot AI-visibility / inbound audit → paid monitoring subscription.

## Locked wedge

**ICP:** B2B SaaS companies with **fewer than 50 employees** (founders / marketing leads).  
Not a generic “track ChatGPT for anyone” wrapper.

## Pricing

- Free: rate-limited single audit (e.g. 3 / IP / day)  
- Paid Starter: **$29/mo** (floor **$19/mo** only if 48h COGS pilot shows margin need)  
- Higher tiers later (agency multi-workspace) — out of MVP scope

## Scorecard override (why not #27 directory/templates)

Directory/templates scored **27** vs GEO **25** on raw totals because of autonomy/OpEx.  
**Override rule:** optimize for **weeks-to-first-dollar + pre-sellable subscription**, not max autonomy-on-paper.  
OpenAlternative-style directories often wait on organic traffic before featured-listing revenue; GEO has live paid comps (Otterly/Livesov) and a free-audit funnel we can ship in ≤3 weeks. Directory remains Plan B / parallel SEO asset only.

## Final MVP acceptance criteria (ordered)

0. **COGS / engines spike (GATE)** — split:
   - **AC#0a (cost model):** ≤3 named engines; 20-prompt design; **labeled ESTIMATE** $/run (FACT list prices × documented quantities OK); Starter limits with ESTIMATE COGS &lt;30% of $29. Unlocks **AC#1** and **AC#2 implementation** on frozen engine IDs only. Does **not** authorize live production engine spend.
   - **AC#0b (measured):** provider `usage` and/or invoice (or bounded `--live` probes with human-approved keys/spend). Required before **LAUNCH**, before enabling live free-audit traffic, and before treating COGS as MEASURED. If measured &gt;2× ESTIMATE or breaks 30%, revise limits or kill. “48h pilot” = cost-model spike + measured validation before launch — not a wall-clock gate for 0a.
1. Public landing page: value prop, ICP, pricing, CTA for free audit.  
2. Free audit: submit brand/URL (+ optional competitors) → citation/visibility breakdown without human review; rate-limited. **Engines MUST be exactly the AC#0a locked set.** Code may land after 0a; **live calls / public traffic** require AC#0b (or explicit human spend approval).  
3. Paid: Stripe Checkout Starter; auth dashboard with run history + scheduled re-checks + weekly email report.  
4. Persist results with timestamps; never invent citations.  
5. Automated tests: invalid input, rate limit, Stripe test checkout session, webhook → subscription active.  
6. No LinkedIn/Reddit automation; no outbound spam features.

## Kill criteria

Day 21 after public LAUNCH: **&lt;10 activated trials** OR measured COGS **&gt;50%** of list at intended Starter usage → pivot wedge or Plan B (directory / utility API / legal data API).

## Reviewer

**ACCEPTED** 2026-09-13 by review agent (2k) under profit-first mission. T3 unlocked; start AC#0. Mission-level PASS still requires `REVENUE.md` net profit > 0.
