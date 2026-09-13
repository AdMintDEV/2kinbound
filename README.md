# Forge

Research in. Ranked opportunities out.

Forge is a local pipeline that accepts research records, calculates a transparent weighted opportunity score, stores both, and shrinks conviction when data is missing instead of pretending the gaps are fine.

## Pipeline

```
JSON research records
        ↓
     validate
        ↓
      score
        ↓
      SQLite
        ↓
  CLI / dashboard
```

Factors and weights:

| Factor | Weight | What it uses |
| --- | --- | --- |
| Market | 0.25 | TAM, growth rate |
| Traction | 0.20 | revenue, users, growth |
| Competition | 0.15 | intensity, incumbent count |
| Timing | 0.15 | urgency, catalysts |
| Risk | 0.15 | listed risk severities |
| Effort | 0.10 | months, cost |

Missing factors are omitted from the raw weighted average. The **adjusted score** is `raw × completeness`, so a hunch with no evidence cannot outrank a documented opportunity.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## Use

```powershell
forge pipeline data/sample_records.json
forge list
forge show tube-chassis
forge serve
```

Dashboard: http://127.0.0.1:8000

API: http://127.0.0.1:8000/docs
