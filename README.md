# 2kinbound

Autonomous multi-agent project to build an internet business targeting **$2,000/month profit**.

## Start here (shared memory)

1. [00_MISSION.md](./00_MISSION.md) — objective and constraints  
2. [01_STATE.md](./01_STATE.md) — current phase and blockers  
3. [04_TASK_QUEUE.md](./04_TASK_QUEUE.md) — team queue  
4. [AGENT_STATE.md](./AGENT_STATE.md) — this operator’s live state  
5. [PAYMENT.md](./PAYMENT.md) — Stripe Payment Link (required to collect money)

Research: `research/`. Decisions: `decisions/`. Reviews: `reviews/`.

**Rule:** Repo beats chat. `REVENUE.md` net &gt; 0 is the only mission PASS.

---

## Public F-path — TubeCheck

Unofficial **FSAE 2026** steel-tube Size A/B/C/D checker and 4130 stick nest. Zero API COGS.

```powershell
python -m http.server 8080 --directory docs
```

http://127.0.0.1:8080 — not SAE, not SES.

$9 Team Pack is sold at a merchant checkout (Payhip or Stripe file attachment). The catalog is not in this public repo. After clone, run `python3 scripts/generate_team_pack.py` and upload the gitignored files under `pack/private/` (`PAYMENT.md`). Paste the checkout URL into `docs/config.js`.

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
