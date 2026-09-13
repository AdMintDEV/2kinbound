# TASK_QUEUE

Statuses: TODO | IN_PROGRESS | BLOCKED | VERIFIED | COMPLETE

## T8 (ACTIVE — P0 revenue)
Objective: Make the $9 Team Pack something people must pay to get  
Status: IN_PROGRESS  
Owner: Builder  
Why it matters: Without this, Stripe/Payhip cannot produce net profit — the SKU is free on Pages  
Required inputs: `reviews/TEST_2026-09-13_TUBECHECK_LIVE.md`, `PAYMENT.md`, `docs/`  
Expected output:
1. Remove `docs/4130-catalog.csv` from public site (or replace with teaser-only sample).
2. `pack.html` no longer serves paid assets in the clear; thank-you page only after purchase.
3. Buy CTA on `index.html` → merchant URL (Payhip digital product preferred; Stripe Payment Link only if delivery is solved).
4. Document human setup steps in `PAYMENT.md` for the chosen rail.
5. Optional P2: `nest()` reject non-positive lengths.
Success criteria: Tester cannot download full pack assets without paying; Buy button opens live checkout when human pastes URL  
Next after: T4b re-test → human paste URL if missing → T9 distribution → first sale

## T9
Objective: Distribution plan for first TubeCheck buyers  
Status: TODO  
Owner: Research  
Success: `research/05_TUBECHECK_DISTRIBUTION.md` with 5–10 concrete channels + draft copy marked needs-human-approval  
Next after: human-approved posts OR organic indexing only

## T3a / AC#0a
Status: COMPLETE (this PR) — ESTIMATE ledger + frozen `openai-web-search` + `perplexity-sonar`. Unlocks AC#1 and AC#2 **code** only.

## T3b / AC#0b
Status: BLOCKED (keys/spend) — required before LAUNCH / live free-audit traffic. Defer until TubeCheck can charge. Do not run `--live` without human-approved keys.

## T3 / AC#1
Status: COMPLETE on this PR — `product/landing/` + gated `/audit` stub (no spend).

## TASK-101..103
VERIFIED locally / shipped (pack integrity still FAIL — T8)

## TASK-104
BLOCKED — human merchant link + T8 delivery redesign

## TASK-105
COMPLETE — https://admintdev.github.io/2kinbound/
