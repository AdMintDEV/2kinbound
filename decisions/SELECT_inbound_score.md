# SELECT: Inbound Score = AI visibility / GEO monitoring

**Status:** READY FOR REVIEWER (not yet ACCEPTED)  
**Date:** 2026-09-13  
**Evidence:** `research/02_DISCOVER_VALIDATE.md` v1.1  
**Remote:** mission + Forge on `main` (`48a1652` — see also `01_STATE.md`)

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

0. **COGS / engines spike (GATE):** 48h pilot — 20 prompts × ≤3 engines; document measured $/run, named engines, and Starter limits so estimated COGS &lt;30% at list price. **Output must name the allowed engines.**  
1. Public landing page: value prop, ICP, pricing, CTA for free audit.  
2. Free audit: submit brand/URL (+ optional competitors) → citation/visibility breakdown without human review; rate-limited. **Engines used in the free audit MUST be exactly the set named in AC#0. Do not ship AC#2 until AC#0 is done and engines + unit COGS are written.**  
3. Paid: Stripe Checkout Starter; auth dashboard with run history + scheduled re-checks + weekly email report.  
4. Persist results with timestamps; never invent citations.  
5. Automated tests: invalid input, rate limit, Stripe test checkout session, webhook → subscription active.  
6. No LinkedIn/Reddit automation; no outbound spam features.

## Kill criteria

Day 21 after public LAUNCH: **&lt;10 activated trials** OR measured COGS **&gt;50%** of list at intended Starter usage → pivot wedge or Plan B (directory / utility API / legal data API).

## Reviewer ask

Mark this file **ACCEPTED** (or file a new FAIL with required deltas). Builder T3 stays blocked until ACCEPTED.
