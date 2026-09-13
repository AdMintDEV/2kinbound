"""Domain models for research records and opportunity scores."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return uuid4().hex[:12]


class EvidenceItem(BaseModel):
    claim: str
    source: str | None = None
    strength: float = Field(default=0.5, ge=0, le=1)


class MarketSignals(BaseModel):
    tam_usd: float | None = Field(default=None, ge=0)
    growth_rate: float | None = None
    notes: str | None = None


class TractionSignals(BaseModel):
    users: int | None = Field(default=None, ge=0)
    revenue_usd: float | None = Field(default=None, ge=0)
    growth_rate: float | None = None


class CompetitionSignals(BaseModel):
    intensity: float | None = Field(default=None, ge=0, le=1)
    incumbent_count: int | None = Field(default=None, ge=0)
    notes: str | None = None


class TimingSignals(BaseModel):
    urgency: float | None = Field(default=None, ge=0, le=1)
    catalysts: list[str] = Field(default_factory=list)


class RiskItem(BaseModel):
    description: str
    severity: float = Field(ge=0, le=1)


class EffortSignals(BaseModel):
    months: float | None = Field(default=None, ge=0)
    cost_usd: float | None = Field(default=None, ge=0)


class ResearchRecord(BaseModel):
    id: str = Field(default_factory=new_id)
    title: str
    summary: str = ""
    source: str = "manual"
    created_at: datetime = Field(default_factory=utcnow)
    market: MarketSignals = Field(default_factory=MarketSignals)
    traction: TractionSignals = Field(default_factory=TractionSignals)
    competition: CompetitionSignals = Field(default_factory=CompetitionSignals)
    timing: TimingSignals = Field(default_factory=TimingSignals)
    risks: list[RiskItem] = Field(default_factory=list)
    effort: EffortSignals = Field(default_factory=EffortSignals)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title is required")
        return cleaned


class FactorScore(BaseModel):
    name: str
    weight: float
    value: float | None
    missing_fields: list[str] = Field(default_factory=list)
    rationale: str


class OpportunityScore(BaseModel):
    record_id: str
    raw_score: float
    adjusted_score: float
    completeness: float
    confidence: float
    missing_fields: list[str]
    factors: list[FactorScore]
    scored_at: datetime = Field(default_factory=utcnow)

    def rank_band(self) -> str:
        if self.adjusted_score >= 75:
            return "strong"
        if self.adjusted_score >= 55:
            return "watch"
        if self.adjusted_score >= 35:
            return "weak"
        return "pass"


class PipelineResult(BaseModel):
    ingested: int
    scored: int
    skipped: int
    errors: list[str] = Field(default_factory=list)
    scores: list[OpportunityScore] = Field(default_factory=list)
