# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

Also mirrored in root `TASK_QUEUE.md`.

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T8 | IN_PROGRESS | Builder | P0: stop free pack leakage; wire merchant delivery for $9 Team Pack |
| T9 | TODO | Research | TubeCheck distribution plan (drafts only; no posting) |
| T4b | TODO | Tester | Re-TEST pack paywall after T8 |
| T5 | TODO | Debugger | FIX failures from T4b |
| T6 | TODO | Reviewer | Review money path vs AC + test evidence |
| T7 | TODO | Builder+ | First sale MEASURE; update REVENUE.md |
| T3b | BLOCKED | Builder | AC#0b measured COGS — needs keys/spend; **required for live free-audit / LAUNCH** |
| T2b | TODO | Research | Plan B refresh after first TubeCheck attempt |

## Done

| ID | Owner | Task |
|----|-------|------|
| T0 | Research | Shared memory on remote |
| T1 | Research | DISCOVER/VALIDATE v1.1 |
| T2 | Research+Reviewer | SELECT ACCEPTED (r3) |
| T3a | Builder+Reviewer | AC#0a ESTIMATE PASS — code may use frozen engines; live traffic still blocked |
| T3 / AC#1 | Builder | Landing + gated `/audit` stub (`product/landing/`) |
| T105 | Builder | GitHub Pages LIVE |
| T4a | Tester | TubeCheck live TEST — FAIL pack integrity (filed) |

## Notes

- Mission PASS requires `REVENUE.md` net > 0.
- Static `?k=` unlock is **killed** as a paywall. Do not pretend client-side tokens are commerce.
- Goal Manager priority: revenue → remove revenue blockers. Skip GEO live spend until money rail works.
- Do **not** claim AC#2 is fully unblocked. AC#0a = implement code; AC#0b = live traffic / LAUNCH.
