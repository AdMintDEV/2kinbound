# AGENT_STATE — Forge toolkit only

**Updated:** 2026-09-13  
**Scope:** This file tracks the **Forge** scoring library under `src/forge/` only.

## ⚠️ Not the team mission

The **2kinbound team objective** ($2k/mo profit business) is **NOT complete**.  
Authoritative status: [`01_STATE.md`](./01_STATE.md) + [`04_TASK_QUEUE.md`](./04_TASK_QUEUE.md) + [`00_MISSION.md`](./00_MISSION.md).

Do **not** treat anything below as permission to skip DISCOVER → BUILD → LAUNCH.

## Forge toolkit objective

Build a verified **research-to-opportunity scoring pipeline** (ingest → score → store → inspect).

**Forge status:** COMPLETE (library/tooling only)

## Definition of Done (Forge only)

- Ingest → score → store → inspect works
- Automated tests pass (20 as of 2026-09-13)
- CLI pipeline works on sample data
- HTTP API + dashboard browser-verified
- Missing-data handling: `adjusted = raw × completeness`
- No blocking Forge bugs

## Requirements (Forge)

1. Accept research records (JSON / CLI / API) — VERIFIED  
2. Transparent weighted opportunity score — VERIFIED  
3. Persist records and scores — VERIFIED  
4. Incomplete data cannot inflate rank — VERIFIED  
5. Unit tests — VERIFIED  
6. Pipeline integration — VERIFIED  
7. CLI + local dashboard — VERIFIED  
8. Failure cases tested — VERIFIED  

## Team next action

See `04_TASK_QUEUE.md` — currently SELECT re-review / Builder T3 still blocked until SELECT **ACCEPTED**.
