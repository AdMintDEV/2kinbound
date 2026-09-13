# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T8 | IN_PROGRESS | Builder+Cloud | Merge PR #3 (delete catalog from tree); PR #2 closed |
| T4b | TODO | Tester | Re-TEST after PR #3 on Pages |
| T10 | BLOCKED | Human | Checkout URL + Draft A post after T8 PASS |
| T7 | TODO | Builder+ | First sale MEASURE |
| T3b | BLOCKED | Builder | AC#0b — parked |

## Done

| ID | Owner | Task |
|----|-------|------|
| T9 | Research | Distribution plan |
| T4a | Tester | Live TEST — FAIL pack integrity |
| T105 | Builder | Pages LIVE |
| T3a | Builder+Reviewer | AC#0a PASS |
| T2 | Research+Reviewer | SELECT ACCEPTED |

## Notes

- PR #2 rejected: `pack_assets/` on a **public** repo is still free via raw.githubusercontent.com.
- PR #3 is the money-rail fix: catalog off the git tree tip; `pack.html` fail-closed; Buy → `paymentUrl`.
