# TASK_QUEUE

## T8
Status: **DONE** — PR #3 merged `615c3f9`. PR #2 closed (public-raw leak).

## T4b (ACTIVE)
Objective: Prove unpaid users cannot get the full Team Pack from live site / main tip  
Owner: Tester  
Success:
1. `https://admintdev.github.io/2kinbound/4130-catalog.csv` → 404
2. `pack.html` has no paid download; `?k=` does nothing
3. Buy disabled/coming-soon while `paymentUrl == ""`
4. Report residual risk from git history raw URLs (note only; no history rewrite unless Goal Manager asks)
Evidence: `reviews/TEST_2026-09-13_T4b.md`
Next: PASS → human merchant URL; FAIL → Debugger T5

## T9
DONE — `research/05_TUBECHECK_DISTRIBUTION.md`

## TASK-104
BLOCKED — human merchant link
