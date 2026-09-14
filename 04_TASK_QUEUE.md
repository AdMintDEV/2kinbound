# Task queue

## Active

| ID | Status | Owner | Task |
|----|--------|-------|------|
| T13 | IN_PROGRESS | Builder | Generate private rotated Team Pack assets (gitignored) for Payhip |
| T10 | BLOCKED | Human | Merchant URL + Draft A |
| T12 | TODO | Tester | Post-wire checkout smoke |
| T7 | TODO | Builder+ | First sale MEASURE |
| T3b | BLOCKED | Builder | AC#0b parked |

## Done

| ID | Owner | Task |
|----|-------|------|
| T11 | Builder+Reviewer | Teaser CATALOG PASS |
| T6 | Reviewer | Money path CONDITIONAL (+ T11 addendum) |
| T4b / T8 / T9 | — | Paywall + distribution |

## Notes

- Sandbox Stripe OK for wiring/tests only — never `REVENUE.md`.
- Prefer public Payment Link / Payhip URL in `config.js`; no secret keys in repo.
