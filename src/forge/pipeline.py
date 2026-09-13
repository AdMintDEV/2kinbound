"""Ingest → validate → score → store pipeline."""

from __future__ import annotations

from pathlib import Path

from forge.ingest import load_records, parse_records
from forge.models import OpportunityScore, PipelineResult, ResearchRecord
from forge.scoring import score_record
from forge.storage import Store


class Pipeline:
    def __init__(self, store: Store | None = None) -> None:
        self.store = store or Store()

    def ingest_records(self, records: list[ResearchRecord]) -> list[ResearchRecord]:
        stored: list[ResearchRecord] = []
        for record in records:
            stored.append(self.store.upsert_record(record))
        return stored

    def score_records(self, records: list[ResearchRecord] | None = None) -> list[OpportunityScore]:
        targets = records if records is not None else self.store.list_records()
        scores: list[OpportunityScore] = []
        for record in targets:
            score = score_record(record)
            self.store.upsert_score(score)
            scores.append(score)
        scores.sort(key=lambda item: item.adjusted_score, reverse=True)
        return scores

    def run_payload(self, payload: object) -> PipelineResult:
        records, errors = parse_records(payload)
        stored = self.ingest_records(records)
        scores = self.score_records(stored)
        return PipelineResult(
            ingested=len(stored),
            scored=len(scores),
            skipped=len(errors),
            errors=errors,
            scores=scores,
        )

    def run_file(self, path: str | Path) -> PipelineResult:
        records, errors = load_records(path)
        stored = self.ingest_records(records)
        scores = self.score_records(stored)
        return PipelineResult(
            ingested=len(stored),
            scored=len(scores),
            skipped=len(errors),
            errors=errors,
            scores=scores,
        )

    def rescore_all(self) -> PipelineResult:
        records = self.store.list_records()
        scores = self.score_records(records)
        return PipelineResult(
            ingested=len(records),
            scored=len(scores),
            skipped=0,
            scores=scores,
        )
