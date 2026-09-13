"""SQLite persistence for research records and opportunity scores."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

from forge.models import OpportunityScore, ResearchRecord

DEFAULT_DB_PATH = Path(os.environ.get("FORGE_DB", str(Path("data") / "forge.db")))

SCHEMA = """
CREATE TABLE IF NOT EXISTS research_records (
    id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS opportunity_scores (
    record_id TEXT PRIMARY KEY,
    payload TEXT NOT NULL,
    adjusted_score REAL NOT NULL,
    scored_at TEXT NOT NULL,
    FOREIGN KEY (record_id) REFERENCES research_records(id)
);
"""


class Store:
    def __init__(self, path: str | Path = DEFAULT_DB_PATH) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _init(self) -> None:
        with self._connect() as connection:
            connection.executescript(SCHEMA)

    def upsert_record(self, record: ResearchRecord) -> ResearchRecord:
        payload = record.model_dump_json()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO research_records (id, payload, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET payload = excluded.payload
                """,
                (record.id, payload, record.created_at.isoformat()),
            )
        return record

    def get_record(self, record_id: str) -> ResearchRecord | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM research_records WHERE id = ?",
                (record_id,),
            ).fetchone()
        if row is None:
            return None
        return ResearchRecord.model_validate_json(row["payload"])

    def list_records(self) -> list[ResearchRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT payload FROM research_records ORDER BY created_at DESC"
            ).fetchall()
        return [ResearchRecord.model_validate_json(row["payload"]) for row in rows]

    def upsert_score(self, score: OpportunityScore) -> OpportunityScore:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO opportunity_scores (record_id, payload, adjusted_score, scored_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(record_id) DO UPDATE SET
                    payload = excluded.payload,
                    adjusted_score = excluded.adjusted_score,
                    scored_at = excluded.scored_at
                """,
                (
                    score.record_id,
                    score.model_dump_json(),
                    score.adjusted_score,
                    score.scored_at.isoformat(),
                ),
            )
        return score

    def get_score(self, record_id: str) -> OpportunityScore | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM opportunity_scores WHERE record_id = ?",
                (record_id,),
            ).fetchone()
        if row is None:
            return None
        return OpportunityScore.model_validate_json(row["payload"])

    def list_scores(self) -> list[OpportunityScore]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload FROM opportunity_scores
                ORDER BY adjusted_score DESC
                """
            ).fetchall()
        return [OpportunityScore.model_validate_json(row["payload"]) for row in rows]

    def scored_pairs(self) -> list[tuple[ResearchRecord, OpportunityScore]]:
        scores = {score.record_id: score for score in self.list_scores()}
        pairs: list[tuple[ResearchRecord, OpportunityScore]] = []
        for record in self.list_records():
            score = scores.get(record.id)
            if score is not None:
                pairs.append((record, score))
        pairs.sort(key=lambda item: item[1].adjusted_score, reverse=True)
        return pairs

    def export_snapshot(self) -> dict:
        return {
            "records": [json.loads(record.model_dump_json()) for record in self.list_records()],
            "scores": [json.loads(score.model_dump_json()) for score in self.list_scores()],
        }
