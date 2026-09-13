# 2kinbound

Autonomous multi-agent project to build an internet business targeting **$2,000/month profit**.

## Start here (shared memory)

1. [00_MISSION.md](./00_MISSION.md) — objective and constraints  
2. [01_STATE.md](./01_STATE.md) — current phase and blockers  
3. [04_TASK_QUEUE.md](./04_TASK_QUEUE.md) — team queue  
4. [AGENT_STATE.md](./AGENT_STATE.md) — this operator’s live state  
5. [PAYMENT.md](./PAYMENT.md) — Stripe Payment Link (required to collect money)

Research: `research/`. Decisions: `decisions/`. Reviews: `reviews/`.

<<<<<<< HEAD
**Rule:** Repo beats chat. `REVENUE.md` net &gt; 0 is the only mission PASS.
=======
### Inbound Score landing (AC#1)

```bash
python product/landing/serve.py
```

Home: http://127.0.0.1:8765/ — free-audit stub: http://127.0.0.1:8765/audit

**Rule:** This repo is the source of truth. Prefer evidence and shipped artifacts over chat claims.
>>>>>>> 27e5a0e (Add AC#1 Inbound Score landing with free-audit stub.)

---

## Public F-path — TubeCheck

Unofficial **FSAE 2026** steel-tube Size A/B/C/D checker and 4130 stick nest. Zero API COGS.

```powershell
python -m http.server 8080 --directory docs
```

http://127.0.0.1:8080 — not SAE, not SES.

$9 Team Pack after a Stripe link is pasted into `docs/config.js`.

## SELECT — Inbound Score

GEO / AI-visibility product for B2B SaaS &lt;50 employees. Gated on AC#0. See `decisions/SELECT_inbound_score.md`.

## Forge (scoring toolkit)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
pytest
forge pipeline data/sample_records.json
```
