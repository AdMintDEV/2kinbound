# T12 TEST — Sandbox money-path CTA smoke

**Tester:** tester agent(2k)
**Date:** 2026-09-14
**Repo tip:** `94df6b7`
**Live:** https://admintdev.github.io/2kinbound/
**paymentUrl (sandbox):** `https://buy.stripe.com/test_14A5kw9274me90UcTcbQY00`

## Verdict: **PASS** (sandbox wiring only)

Money-path smoke is green on live Pages. **This is not mission PASS.** Sandbox / test-mode Stripe charges are **not** revenue and must not be written to `REVENUE.md` as profit.

## Checks

| # | Check | Result | Evidence |
|---|--------|--------|----------|
| 1 | Live `config.js` contains the test_ URL | **PASS** | `curl` live config shows exact `buy.stripe.com/test_14A5kw9274me90UcTcbQY00` |
| 2 | Buy CTA opens Stripe checkout (not a free file) | **PASS** | Live `setupPay()` sets `btn.href = cfg.paymentUrl` when set; simulated href is Stripe test link, not `4130-catalog.csv` |
| 3 | `pack.html` fail-closed; `?k=` noop | **PASS** | No catalog download links in live HTML; `isPackUnlocked` always false; `?k=2k4130pack` → state `checkout` (message only); `?paid=1` → `thanks` (still no files) |
| 4 | CSV still 404 on Pages | **PASS** | `https://admintdev.github.io/2kinbound/4130-catalog.csv` → **HTTP 404** |
| 5 | Sandbox ≠ revenue | **PASS (explicit)** | URL is `test_` Payment Link; Stripe checkout **200**; **do not** credit `REVENUE.md` |

## Automated

- `pytest tests/test_pack_integrity.py` → **7 passed**
- Tip has no `docs/4130-catalog.csv`

## Adversarial notes (not FAIL)

1. Static HTML default `#buy` href is still `./pack.html` until `DOMContentLoaded`/`setupPay` runs. With JS (normal path) it becomes Stripe. Noscript users land on the fail-closed pack status page — not a free catalog.
2. Git-history raw-by-SHA residual from T4b remains (P2); rotate merchant file before live charges.
3. No end-to-end paid delivery verified (Payhip/Stripe file attachment). T12 scope is CTA + fail-closed site only.

## Mission

**FAIL / not applicable** for first-dollar profit. T12 PASS ≠ `REVENUE.md` net > 0.

## Recommendation

- Warden: accept T12 PASS; keep TubeCheck on path to **live** (non-test) Payment Link + real receipt before any revenue claim.
- No Debugger T5.
