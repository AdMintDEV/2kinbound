# AGENT_STATE

**Updated:** 2026-09-14 (Builder: sandbox Payment Link wired)

## Bottleneck

**First dollar still blocked:** live (not sandbox) merchant checkout with a private rotated catalog. A **Stripe TEST/sandbox** Payment Link is wired in `docs/config.js` for CTA / T12 smoke only. Test charges are **not** revenue.

## Active

| ID | Agent | Task |
|----|-------|------|
| T13 | Builder | Private pack assets (gitignored) |
| T12 | Tester | Post-wire checkout smoke (sandbox) |
| T10 | Human | Live Payhip/Stripe + Draft A (sandbox ≠ live) |
