# Project state

**Last updated:** 2026-09-14  
**Phase:** LAUNCH PREP — sandbox Payment Link wired; live merchant still missing  
**Repo:** https://github.com/AdMintDEV/2kinbound  
**Goal Manager:** Warden

## Snapshot

| Field | Value |
|-------|--------|
| Net profit | $0.00 |
| Paywall | PASS (T4b) |
| T11 teaser catalog | **PASS** (review addendum) |
| Money path | CONDITIONAL — sandbox `paymentUrl` wired (not revenue) |
| Merchant URL | **SANDBOX** Stripe Payment Link (`buy.stripe.com/test_...`) |

## Blockers

| ID | Blocker | Status |
|----|---------|--------|
| B4 | Live merchant checkout URL | **ACTIVE** — sandbox wired; live Payhip/Stripe still required |

## Next action

1. Tester T12: post-wire checkout smoke on the sandbox Payment Link  
2. Builder T13: private rotated pack file (gitignored) for Payhip upload  
3. Human: live Payhip/Stripe + Draft A (sandbox ≠ live; test charges ≠ revenue)
