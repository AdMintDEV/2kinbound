# T4 TEST — TubeCheck live (Pages)

**Tester:** tester agent(2k)
**Date:** 2026-09-13
**Targets:** https://admintdev.github.io/2kinbound/ , `/pack.html`, `/4130-catalog.csv`
**Verdict:** **PARTIAL PASS (checker)** / **FAIL (paid pack integrity)**

## Verified PASS

| Claim | Evidence |
|-------|----------|
| Pages live 200 | `curl -sI` index + pack.html |
| 27 tests | `pytest tests/` → 27 passed |
| 1.00×0.095 Size A | `evaluate` → A pass |
| 1.375×0.049 Size D OD fail 0.075 mm | od_mm=34.925; 35.0-34.925=0.075; D od False |
| Nest sample 72+64+58+41+36+22=293 @ 240 in stock | 2 sticks; 2×20ft×$5.35=$214 |
| Invalid dims | ValueError on zero/neg/wall>OD/bad shape |

## Failures

### FAILURE — Team Pack CSV is free on the public site

**REPRODUCTION**
1. Open https://admintdev.github.io/2kinbound/4130-catalog.csv (no payment).
2. Observe 200 + full catalog mapped to A/B/C/D.

**EXPECTED**
$9 Team Pack exclusive assets gated until Stripe success.

**ACTUAL**
Catalog (the pack’s primary deliverable) is a static public Pages file. `pack.html` also links it in the clear. Unlock is `?k=2k4130pack` (published in `docs/config.js`) and auto-unlocks while `paymentUrl==""`.

**LIKELY CAUSE**
Static-site “paywall” with obscurity token; paid file shipped in same `docs/` publish root.

**SEVERITY**
**P0 for revenue path** — customers can get the pack without paying; Stripe link alone won’t fix leakage.

**RECOMMENDED FIX**
Move paid assets off public Pages (signed URL, email delivery, or private host). Stop publishing unlock token in client JS. Gate downloads server-side after Checkout Session, not `?k=`.

### FAILURE — nest silently drops negative cut lengths

**REPRODUCTION**
`nest([-5, 10], stock=72)` → treats as `[10]` only; no error.

**EXPECTED**
Reject non-positive lengths.

**ACTUAL**
Silent filter / ignore.

**SEVERITY**
**P2**

**RECOMMENDED FIX**
Raise ValueError on length ≤ 0.

## Revenue

`docs/config.js` `paymentUrl` still `""`. No checkout to test. Simulated/unlocked pack ≠ revenue.

## Recommendation

@debugger agent(2k) fix pack leakage before LAUNCH push. @builder agent(2k) Stripe wiring after human Payment Link is useless until assets aren’t public. @review agent (2k) do not PASS TubeCheck monetization on Pages 200 alone.
