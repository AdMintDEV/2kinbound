# Project state

**Last updated:** 2026-09-13  
**Phase:** LAUNCH PREP (first dollar) — TubeCheck live; leakage fix on T8 branch  
**Repo:** https://github.com/AdMintDEV/2kinbound  
**Goal Manager:** Warden

## Snapshot

| Field | Value |
|-------|--------|
| Mission | First legitimate **net profit** ($0.01+), then scale to $2,000/mo |
| Selected experiment | **ACCEPTED:** Inbound Score (GEO) — B2B SaaS <50 |
| Parallel F-path | **TubeCheck** — public Pages LIVE |
| Product URL | https://admintdev.github.io/2kinbound/ |
| Net profit | $0.00 — see `REVENUE.md` |
| Cloud agent / `gh` | YES |

## Blockers

| ID | Blocker | Status |
|----|---------|--------|
| B3 | SELECT not ACCEPTED | **RESOLVED** — ACCEPTED r3 |
| B4 | Merchant checkout for TubeCheck | **ACTIVE** — human Payment Link / Payhip (`PAYMENT.md`) |
| B5 | Pack assets public on Pages | **RESOLVED on this branch** — full CSV in `pack_assets/` (not Pages); Buy disabled until `paymentUrl` set |
| — | GEO engine spend (AC#0b) | Needs human keys; **not** on first-dollar critical path |

## Next action

1. **Tester T4b:** confirm unpaid visitors cannot fetch pack assets from Pages; empty `paymentUrl` does not unlock.
2. **Human:** create $9 checkout that hosts/delivers the pack (Payhip easiest). Paste URL.
3. **Research T9:** distribution plan (no posting without approval).
