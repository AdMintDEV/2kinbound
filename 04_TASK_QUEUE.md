# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

Also mirrored in root `TASK_QUEUE.md`.

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T8 | IN_PROGRESS | Builder | P0: stop free pack leakage; wire merchant delivery for $9 Team Pack |
| T4b | TODO | Tester | Re-TEST pack paywall after T8 |
| T5 | TODO | Debugger | FIX failures from T4b |
| T6 | TODO | Reviewer | Review money path vs AC + test evidence |
| T7 | TODO | Builder+ | First sale MEASURE; update REVENUE.md |
| T10 | BLOCKED | Human | Approve + post Draft A (r/FSAE) after T8 PASS + merchant URL |
| T3b | BLOCKED | Builder | AC#0b measured COGS — needs keys/spend |
| T2b | TODO | Research | Plan B refresh after first TubeCheck attempt |

## Done

| ID | Owner | Task |
|----|-------|------|
| T0 | Research | Shared memory on remote |
| T1 | Research | DISCOVER/VALIDATE v1.1 |
| T2 | Research+Reviewer | SELECT ACCEPTED (r3) |
| T3a | Builder+Reviewer | AC#0a ESTIMATE PASS |
| T105 | Builder | GitHub Pages LIVE |
| T4a | Tester | TubeCheck live TEST — FAIL pack integrity (filed) |
| T9 | Research | Distribution plan — `research/05_TUBECHECK_DISTRIBUTION.md` |

## Notes

- Mission PASS requires `REVENUE.md` net > 0.
- After T8: human checkout URL → T4b → approve Draft A only (no agent posting).
- Goal Manager priority: revenue → remove revenue blockers.
