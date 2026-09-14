# Kill My Idea — TubeCheck

**Date:** 2026-09-14  
**Status:** OPEN — sandbox money path green; live merchant still missing  
**Author:** Research Agent (2k) — T16 refresh

## Claim
$9 Team Pack + free FSAE 2026 Size A–D checker can produce the first legitimate **net** profit from tube-frame teams.

## FOR
- Checker LIVE 200; Tester verified Size A / Size D −0.075 mm / nest (`reviews/TEST_2026-09-13_TUBECHECK_LIVE.md`).
- Pack leakage closed on tip/Pages: `/4130-catalog.csv` **404** (T8/T4b; reconfirmed T12).
- Free CATALOG teaser ≤4 rows PASS (T11 — `reviews/REVIEW_2026-09-13_MONEY_PATH_T11.md`).
- Private rotated pack generator under `pack/private/` (T13).
- Sandbox CTA wiring PASS: live `paymentUrl` → `buy.stripe.com/test_…`; Buy opens checkout, not a free file; pack fail-closed (`reviews/TEST_2026-09-14_T12_SANDBOX_CTA.md`).
- $0 API COGS on checker; distribution plan ready (`research/05_TUBECHECK_DISTRIBUTION.md`).
- ICP exists (FSAE tube teams).

## AGAINST
- **Live (non-test) merchant URL still missing** — cannot take real money.
- Sandbox / test charges **≠ revenue** (explicit T12); `REVENUE.md` still **$0**.
- End-to-end paid **file delivery** not verified (Payhip attach / post-pay email).
- Residual P2: historical raw-by-SHA catalog exposure (T4b note) — rotate before live charges.
- Willingness to pay vs free official SES still **UNKNOWN**.
- No approved distribution yet; Draft A **held** (must not advertise sandbox Buy).

## Verdict
**SURVIVES** as product bet.  
**PIVOT (go-to-market):** treat current state as **pre-revenue plumbing**. Soft-launch **free checker only** is allowed; **do not** market the $9 Buy until a live Payment Link/Payhip is live and delivery works.  
No third product. No ads. No Draft A until live merchant.

## Soft-launch free checker only (no Buy mention)?
**Yes.** Copy: **Draft A-free** in `research/05_TUBECHECK_DISTRIBUTION.md` (no Buy / no pack / no sandbox Stripe). Reason: T12 proves the site is safe to show (CSV 404, fail-closed pack), but advertising a `test_` Stripe Buy trains the wrong habit and cannot produce `REVENUE.md` net profit. A free-tool-only Draft A (link + disclaimers, no pack CTA) can collect feedback/signals while human finishes live merchant + delivery — without claiming a paid product that cannot clear real dollars.

## Change-verdict criteria
- → **Stronger SURVIVES / scale:** first **live** $9 net of fees in `REVENUE.md` + delivery confirmed.
- → **KILL paid pack** (keep free checker): 14 days after live merchant + ≥1 approved post with measurable traffic and **zero** checkout intent / refunds dominate.
- → **KILL whole TubeCheck:** repeated technical FAIL on live Pages after fixes, or ICP rejects unofficial tools in feedback logs.

## Evidence links
- `reviews/TEST_2026-09-13_TUBECHECK_LIVE.md` (original leak FAIL — historical)
- `reviews/TEST_2026-09-13_T4b.md` / PR #3 close
- `reviews/REVIEW_2026-09-13_MONEY_PATH.md`
- `reviews/REVIEW_2026-09-13_MONEY_PATH_T11.md`
- `reviews/TEST_2026-09-14_T12_SANDBOX_CTA.md`
- `research/05_TUBECHECK_DISTRIBUTION.md`
- `PAYMENT.md`, live https://admintdev.github.io/2kinbound/
