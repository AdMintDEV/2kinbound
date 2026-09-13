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
Notes: Catalog must leave the git tree (not just `docs/`). `pack.html` fail-closed. Live Pages still leaks until merge + redeploy. Still blocked on human merchant URL.  
Next after: T4b re-test → human paste URL if missing → T9 distribution → first sale

## T9
Objective: Distribution plan for first TubeCheck buyers  
Status: COMPLETE  
Owner: Research  
Success: `research/05_TUBECHECK_DISTRIBUTION.md` with 5–10 concrete channels + draft copy marked needs-human-approval  
Output: `research/05_TUBECHECK_DISTRIBUTION.md`; Kill stubs in `experiments/active/`  
Next after: T8 PASS → human approves Draft A/B/C → post → log `market/customer_signals/`

## T3b / AC#0b
Status: BLOCKED (keys/spend) — defer until TubeCheck can charge

## TASK-101..103
VERIFIED locally / shipped (pack integrity still FAIL — T8)

## TASK-104
BLOCKED — human merchant link + T8 delivery redesign

## TASK-105
COMPLETE — https://admintdev.github.io/2kinbound/
