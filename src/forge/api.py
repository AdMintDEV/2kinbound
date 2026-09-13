"""HTTP API and local dashboard."""

from __future__ import annotations

from pathlib import Path

from typing import Any

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from forge.dashboard import DASHBOARD_HTML
from forge.models import OpportunityScore, PipelineResult, ResearchRecord
from forge.pipeline import Pipeline
from forge.storage import DEFAULT_DB_PATH, Store


class OpportunityView(BaseModel):
    record: ResearchRecord
    score: dict


class OpportunityList(BaseModel):
    items: list[OpportunityView]


def create_app(db_path: str | Path | None = None) -> FastAPI:
    store = Store(db_path or DEFAULT_DB_PATH)
    pipeline = Pipeline(store)
    app = FastAPI(title="Forge", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", response_class=HTMLResponse)
    def dashboard() -> str:
        return DASHBOARD_HTML

    @app.post("/api/records", response_model=ResearchRecord)
    def create_record(record: ResearchRecord) -> ResearchRecord:
        stored = pipeline.ingest_records([record])[0]
        pipeline.score_records([stored])
        return stored

    @app.get("/api/records", response_model=list[ResearchRecord])
    def list_records() -> list[ResearchRecord]:
        return store.list_records()

    @app.get("/api/records/{record_id}", response_model=ResearchRecord)
    def get_record(record_id: str) -> ResearchRecord:
        record = store.get_record(record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="unknown record")
        return record

    @app.get("/api/scores", response_model=list[OpportunityScore])
    def list_scores() -> list[OpportunityScore]:
        return store.list_scores()

    @app.get("/api/scores/{record_id}", response_model=OpportunityScore)
    def get_score(record_id: str) -> OpportunityScore:
        score = store.get_score(record_id)
        if score is None:
            raise HTTPException(status_code=404, detail="unknown score")
        return score

    @app.get("/api/opportunities", response_model=OpportunityList)
    def list_opportunities() -> OpportunityList:
        items = []
        for record, score in store.scored_pairs():
            payload = score.model_dump(mode="json")
            payload["band"] = score.rank_band()
            items.append(OpportunityView(record=record, score=payload))
        return OpportunityList(items=items)

    @app.post("/api/pipeline", response_model=PipelineResult)
    def run_pipeline(payload: Any = Body(...)) -> PipelineResult:
        result = pipeline.run_payload(payload)
        if result.ingested == 0:
            raise HTTPException(status_code=400, detail={"errors": result.errors})
        return result

    @app.post("/api/pipeline/rescore", response_model=PipelineResult)
    def rescore() -> PipelineResult:
        return pipeline.rescore_all()

    return app


app = create_app()
