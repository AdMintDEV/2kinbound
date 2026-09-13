# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T0 | IN_PROGRESS | Research | Reconcile remote Forge + local mission; push merged `main` (needs GitHub auth). Do **not** force-push. |
| T1 | DONE | Research | DISCOVER → VALIDATE v1.1 |
| T2 | TODO | Research | SELECT: lock wedge; paste final AC into decisions; document scorecard override; mark ACCEPTED only after Reviewer re-check |
| T2b | TODO | Research | Plan B dataset/directory shortlist |
| T3 | BLOCKED | Builder | BUILD MVP — blocked until T0 on remote **and** T2 ACCEPTED by Reviewer |
| T4 | TODO | Tester | Adversarial TEST of MVP |
| T5 | TODO | Debugger | FIX failures |
| T6 | TODO | Reviewer | Re-review after T0+T2 |
| T7 | TODO | Builder+ | LAUNCH + MEASURE |

## Done

| ID | Owner | Task |
|----|-------|------|
| T1 | Research | Sourced DISCOVER/VALIDATE |
| — | Reviewer | REVIEW FAIL documented in `reviews/REVIEW_2026-09-13_SELECT.md` |

## Notes

- Prefer merge over force-push so Forge code is preserved.
- Builder holds T3 until Reviewer PASS for unlock.
