# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T4b | IN_PROGRESS | Tester | Adversarial re-TEST pack paywall on live Pages + main tip |
| T5 | TODO | Debugger | FIX failures from T4b (if any) |
| T6 | TODO | Reviewer | Review money path vs evidence after T4b |
| T10 | BLOCKED | Human | Merchant URL + Draft A post |
| T7 | TODO | Builder+ | First sale MEASURE; update REVENUE.md |
| T3b | BLOCKED | Builder | AC#0b — parked |

## Done

| ID | Owner | Task |
|----|-------|------|
| T8 | Builder+Cloud | Pack leak closed — PR #3 `615c3f9`; PR #2 closed |
| T9 | Research | Distribution plan |
| T4a | Tester | Live TEST — FAIL (drove T8) |
| T105 | Builder | Pages LIVE |
| T3a | Builder+Reviewer | AC#0a PASS |
| T2 | Research+Reviewer | SELECT ACCEPTED |

## Notes

- History may still contain old CSV blobs; tip + Pages must not. T4b should try known raw/history URLs and report residual risk.
- Do not re-ask human for checkout in a loop; blocker remains B4 until they paste a URL.
