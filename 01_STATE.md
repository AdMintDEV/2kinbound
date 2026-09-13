# Project state

**Last updated:** 2026-09-13  
**Phase:** SELECT (reconcile remote; SELECT still PROPOSED)  
**Repo:** https://github.com/AdMintDEV/2kinbound

## Snapshot

| Field | Value |
|-------|--------|
| Selected opportunity | **PROPOSED:** Inbound Score = AI visibility/GEO monitor — free audit → $29/mo (COGS-dependent) |
| Plan B | Niche directory / utility API / legal comps API |
| Product URL | NONE |
| Revenue (MRR / profit) | $0 |
| Local shared memory | YES (mission/state/queue/research/reviews) |
| Remote `origin/main` (pre-push) | **Forge** pipeline only (`7cb9ea4`) — diverged from local |
| Local reconcile | IN PROGRESS — unrelated-histories merge (Forge + mission) on `main`; `forge-archive` points at `7cb9ea4` |
| Cloud agent usable | YES against remote, but **wrong tree** until merged mission is pushed |
| GitHub auth on box | NOT LOGGED IN (blocks push) |

## Blockers

| ID | Blocker | Type | Owner |
|----|---------|------|-------|
| B1 | Remote/main was Forge-only; local was mission-only | Reconcile | Research: merge done locally; needs push |
| B2 | Box not signed into GitHub / `gh auth` | External | User sign-in |
| B3 | SELECT still PROPOSED (wedge + final AC) | Process | Research T2 → Reviewer |

## Decisions

- `decisions/SELECT_inbound_score.md` — PROPOSED
- `reviews/REVIEW_2026-09-13_SELECT.md` — FAIL (T3 locked)

## Metrics (post-LAUNCH)

- Visitors / signups / paid conversions / churn / profit: UNKNOWN
