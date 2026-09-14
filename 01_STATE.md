# Project state

**Last updated:** 2026-09-14  
**Phase:** LAUNCH PREP — code ready; merchant URL missing  
**Repo:** https://github.com/AdMintDEV/2kinbound  
**Goal Manager:** Warden

## Snapshot

| Field | Value |
|-------|--------|
| Net profit | $0.00 |
| Paywall | PASS (T4b) |
| T11 teaser catalog | **PASS** (review addendum) |
| Money path | CONDITIONAL — `paymentUrl` empty |
| Merchant URL | **MISSING** |
| T13 private pack generator | **DONE** (run locally; `pack/private/` gitignored) |

## Blockers

| ID | Blocker | Status |
|----|---------|--------|
| B4 | Merchant checkout URL | **ACTIVE** — human |

## Next action

1. Human: `python scripts/generate_team_pack.py`, upload `pack/private/` in Payhip, paste checkout URL  
2. Builder: wire `paymentUrl` → Draft A (idle until paste)
