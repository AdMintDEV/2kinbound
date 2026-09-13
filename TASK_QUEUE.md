# TASK_QUEUE

Statuses: TODO | IN_PROGRESS | BLOCKED | VERIFIED | COMPLETE

## T8 (DONE on this branch — P0 revenue)
Objective: Make the $9 Team Pack something people must pay to get  
Status: DONE  
Owner: Builder  
Why it matters: Without this, Stripe/Payhip cannot produce net profit — the SKU was free on Pages  
Done:
1. Moved full `4130-catalog.csv` to `pack_assets/` (outside Pages `docs/` publish path).
2. `pack.html` is thank-you only — no paid catalog links/downloads; no `?k=` / empty-`paymentUrl` unlock.
3. Buy CTA uses `paymentUrl` when set; empty URL shows disabled “checkout coming soon”.
4. `PAYMENT.md` updated: upload from `pack_assets/`; success URL thank-you only.
5. P2: `nest()` raises ValueError on non-positive lengths + test.
Success criteria: Tester cannot download full pack assets without paying; Buy button opens live checkout when human pastes URL  
Next after: **T4b re-test** → human paste URL if missing → T9 distribution → first sale

## T4b
Objective: Adversarial re-TEST of pack paywall after T8  
Status: TODO  
Owner: Tester  
Success: Cannot fetch full pack from Pages unpaid; empty `paymentUrl` does not unlock; Buy uses URL when set  
Next after: T5 if FAIL, else human checkout URL + T9

## T9
Objective: Distribution plan for first TubeCheck buyers  
Status: TODO  
Owner: Research  
Success: `research/05_TUBECHECK_DISTRIBUTION.md` with 5–10 concrete channels + draft copy marked needs-human-approval  
Next after: human-approved posts OR organic indexing only

## T3b / AC#0b
Status: BLOCKED (keys/spend) — defer until TubeCheck can charge

## TASK-101..103
VERIFIED locally / shipped (pack integrity addressed by T8 — T4b confirms)

## TASK-104
BLOCKED — human merchant link (T8 delivery redesign done on this branch)

## TASK-105
COMPLETE — https://admintdev.github.io/2kinbound/
