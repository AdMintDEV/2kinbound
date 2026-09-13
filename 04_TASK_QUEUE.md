# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T0 | IN_PROGRESS | Research | Seed `00_MISSION.md`, `01_STATE.md`, `04_TASK_QUEUE.md`, README; push initial commit so cloud agents can run |
| T1 | IN_PROGRESS | Research | DISCOVER → VALIDATE: evidence-backed opportunities; write `research/02_DISCOVER_VALIDATE.md` + scorecard |
| T2 | TODO | Research | SELECT primary opportunity; record decision; draft BUILD acceptance criteria |
| T3 | TODO | Builder | BUILD MVP for selected opportunity (smallest shippable paid surface) |
| T4 | TODO | Tester | Adversarial TEST of MVP against written AC |
| T5 | TODO | Debugger | FIX failures filed by Tester (as needed) |
| T6 | TODO | Reviewer | REVIEW against objective / requirements / AC / behavior / tests |
| T7 | TODO | Builder+ | LAUNCH + MEASURE (real distribution + revenue instrumentation) |

## Done

_None yet (files exist locally; not on remote until first push)._

## Notes

- Do not mark LAUNCH until something customers can pay for is live and measurable.
- Builder waits for T2 acceptance criteria before T3.
