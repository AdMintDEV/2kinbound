# Task queue

Statuses: `TODO` | `IN_PROGRESS` | `DONE` | `BLOCKED`

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T0 | BLOCKED | Research | Push seed commit to `AdMintDEV/2kinbound` (needs GitHub auth on box) |
| T1 | DONE | Research | DISCOVER → VALIDATE v1 in `research/02_DISCOVER_VALIDATE.md` + scorecard |
| T2 | TODO | Research | SELECT: write `decisions/SELECT_inbound_score.md`; confirm AC with Reviewer |
| T2b | TODO | Research | Plan B: shortlist legal datasets for comps-style API |
| T3 | TODO | Builder | BUILD Inbound Score MVP per AC in research doc (after T2 / Reviewer OK) |
| T4 | TODO | Tester | Adversarial TEST of MVP against AC |
| T5 | TODO | Debugger | FIX failures from Tester |
| T6 | TODO | Reviewer | REVIEW objective → requirements → AC → behavior → tests |
| T7 | TODO | Builder+ | LAUNCH + MEASURE |

## Done

| ID | Owner | Task |
|----|-------|------|
| T1 | Research | Sourced DISCOVER/VALIDATE written locally |

## Notes

- Do not start T3 until T0 unblocked (files on remote) OR Builder works from local `/workspace/2kinbound` with explicit sync plan.
- Prefer Stripe test mode until LAUNCH.
