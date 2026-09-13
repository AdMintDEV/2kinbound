from pathlib import Path

from fastapi.testclient import TestClient

from forge.api import create_app
from forge.dashboard import DASHBOARD_HTML


def test_dashboard_defines_render_helpers() -> None:
    assert "function escapeHtml" in DASHBOARD_HTML
    assert "function bandClass" in DASHBOARD_HTML


def test_health_and_pipeline_roundtrip(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "forge.db"))
    assert client.get("/health").json() == {"status": "ok"}
    assert "Forge" in client.get("/").text

    created = client.post("/api/records", json={"title": "From API"})
    assert created.status_code == 200
    record_id = created.json()["id"]
    assert client.get(f"/api/scores/{record_id}").status_code == 200

    scored = client.post("/api/pipeline/rescore")
    assert scored.status_code == 200
    assert scored.json()["scored"] == 1

    listing = client.get("/api/opportunities")
    assert listing.status_code == 200
    items = listing.json()["items"]
    assert items[0]["record"]["id"] == record_id
    assert "band" in items[0]["score"]

    payload = client.post(
        "/api/pipeline",
        json={"records": [{"id": "batch-1", "title": "Batch item"}]},
    )
    assert payload.status_code == 200
    assert payload.json()["ingested"] == 1


def test_api_failure_cases(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "forge.db"))
    assert client.get("/api/records/nope").status_code == 404
    assert client.get("/api/scores/nope").status_code == 404
    bad = client.post("/api/pipeline", json={"hello": "world"})
    assert bad.status_code == 400
    empty = client.post("/api/pipeline", json=[])
    assert empty.status_code == 400
