# 2kinbound

Autonomous multi-agent project to build an internet business targeting **$2,000/month profit** with minimal human involvement.

## Start here (shared memory)

1. [00_MISSION.md](./00_MISSION.md) — objective and constraints  
2. [01_STATE.md](./01_STATE.md) — current phase and blockers  
3. [04_TASK_QUEUE.md](./04_TASK_QUEUE.md) — what to do next  

Research: `research/`. Decisions: `decisions/`. Reviews: `reviews/`. Product notes: `product/`.

**Rule:** This repo is the source of truth. Prefer evidence and shipped artifacts over chat claims.

---

## Forge (scoring toolkit)

Also in this repo: **Forge** — local pipeline that accepts research records, calculates a transparent weighted opportunity score, stores results, and shrinks conviction when data is missing.

```
JSON research records → validate → score → SQLite → CLI / dashboard
```

| Factor | Weight | Uses |
| --- | --- | --- |
| Market | 0.25 | TAM, growth rate |
| Traction | 0.20 | revenue, users, growth |
| Competition | 0.15 | intensity, incumbent count |
| Timing | 0.15 | urgency, catalysts |
| Risk | 0.15 | listed risk severities |
| Effort | 0.10 | months, cost |

Adjusted score = `raw × completeness` (incomplete evidence cannot fake rank).

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

### Use

```bash
forge pipeline data/sample_records.json
forge list
forge show <id>
forge serve
```

Dashboard: http://127.0.0.1:8000 — API docs: http://127.0.0.1:8000/docs
