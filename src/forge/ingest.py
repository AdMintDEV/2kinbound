"""Load research records from JSON files or in-memory payloads."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from forge.models import ResearchRecord


class IngestError(ValueError):
    pass


def _coerce_items(payload: Any) -> list[Any]:
    if payload is None:
        raise IngestError("payload is empty")
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if "records" in payload and isinstance(payload["records"], list):
            return payload["records"]
        return [payload]
    raise IngestError("JSON must be an object, a list, or {\"records\": [...]}")


def parse_records(payload: Any) -> tuple[list[ResearchRecord], list[str]]:
    records: list[ResearchRecord] = []
    errors: list[str] = []
    try:
        items = _coerce_items(payload)
    except IngestError as exc:
        return [], [str(exc)]

    if not items:
        return [], ["no research records found"]

    for index, item in enumerate(items):
        try:
            records.append(ResearchRecord.model_validate(item))
        except ValidationError as exc:
            errors.append(f"record[{index}]: {exc.errors()[0]['msg']}")
        except Exception as exc:  # pragma: no cover - defensive
            errors.append(f"record[{index}]: {exc}")
    return records, errors


def load_records(path: str | Path) -> tuple[list[ResearchRecord], list[str]]:
    file_path = Path(path)
    if not file_path.exists():
        return [], [f"file not found: {file_path}"]
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        return [], [f"could not read {file_path}: {exc}"]
    if not text.strip():
        return [], ["file is empty"]
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return [], [f"invalid JSON: {exc.msg}"]
    return parse_records(payload)
