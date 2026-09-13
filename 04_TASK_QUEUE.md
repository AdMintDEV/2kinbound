# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T2 | IN_PROGRESS | Research → Reviewer | r2 deltas fixed (AGENT_STATE scoped, HEAD refs, AC#0 gates AC#2); awaiting ACCEPTED |
| T2b | TODO | Research | Plan B: directory / utility API / legal comps shortlist |
| T3 | BLOCKED | Builder | BUILD Inbound Score MVP — unlock only after Reviewer ACCEPTED on T2 |
| T4 | TODO | Tester | Adversarial TEST of MVP |
| T5 | TODO | Debugger | FIX failures |
| T6 | TODO | Reviewer | Re-review T0+T2 (PASS required to unlock T3) |
| T7 | TODO | Builder+ | LAUNCH + MEASURE |

## Done

| ID | Owner | Task |
|----|-------|------|
| T0 | Research | Merged Forge + mission; pushed `be842e8` to `origin/main` |
| T1 | Research | DISCOVER → VALIDATE v1.1 |
| — | Reviewer | Prior FAIL documented (`reviews/REVIEW_2026-09-13_SELECT.md`) |

## Notes

- Do not force-push. Forge toolkit retained under `src/forge/`.
- Builder holds T3 until Reviewer ACCEPTED.
