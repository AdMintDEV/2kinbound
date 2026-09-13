"""Team Pack exclusives must not be public on Pages or in this git repo."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tubecheck.pack_gate import is_pack_unlocked, pack_page_state

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "dist", "build", "htmlcov"}
PAID_FILENAMES = {"4130-catalog.csv"}


def _js_call(fn: str, cfg: dict, params: dict):
    script = (
        "const api = require(require('path').join(process.argv[1], 'docs', 'pack.js'));"
        "const cfg = JSON.parse(process.argv[2]);"
        "const params = JSON.parse(process.argv[3]);"
        f"process.stdout.write(JSON.stringify(api.{fn}(cfg, params)));"
    )
    result = subprocess.run(
        ["node", "-e", script, str(ROOT), json.dumps(cfg), json.dumps(params)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _tracked_paths() -> list[str]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [p.decode() for p in raw.split(b"\0") if p]


def _catalog_header() -> str:
    return ",".join(
        ["shape", "od_in", "wall_in", "area_mm2", "I_mm4", "lb_ft", "A", "B", "C", "D"]
    )


def _walk_repo_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def test_paid_catalog_not_in_pages_publish_root() -> None:
    assert not (DOCS / "4130-catalog.csv").exists()
    assert list(DOCS.rglob("*.csv")) == []


def test_paid_catalog_not_in_repo_at_any_published_path() -> None:
    """Public repo: every tracked path is a download. Off-Pages is not enough."""
    tracked = _tracked_paths()
    named = [rel for rel in tracked if Path(rel).name.lower() in PAID_FILENAMES]
    assert named == [], f"paid catalog still tracked: {named}"

    header = _catalog_header()
    content_hits: list[str] = []
    for rel in tracked:
        if not rel.lower().endswith(".csv"):
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        if header in text:
            content_hits.append(rel)
    assert content_hits == [], f"catalog CSV contents still tracked: {content_hits}"

    working = [
        str(path.relative_to(ROOT))
        for path in _walk_repo_files()
        if path.name.lower() in PAID_FILENAMES
    ]
    assert working == [], f"paid catalog still on disk: {working}"


HISTORICAL_PAID_CATALOG_ROWS = 19  # deleted public CSV + former free CATALOG length
FREE_CATALOG_TEASER_MAX = 4


def _free_catalog_rows() -> list:
    script = (
        "const fs = require('fs');"
        "const path = require('path');"
        "const src = fs.readFileSync(path.join(process.argv[1], 'docs', 'app.js'), 'utf8');"
        "const m = src.match(/const CATALOG = (\\[[\\s\\S]*?\\]);/);"
        "if (!m) { process.stderr.write('CATALOG missing'); process.exit(2); }"
        "process.stdout.write(JSON.stringify(eval(m[1])));"
    )
    result = subprocess.run(
        ["node", "-e", script, str(ROOT)],
        check=True,
        capture_output=True,
        text=True,
    )
    rows = json.loads(result.stdout)
    assert isinstance(rows, list)
    return rows


def test_free_docs_catalog_is_teaser_not_full_map() -> None:
    """Unpaid visitors must not reconstruct the paid Size A/B/C/D catalog from Pages."""
    rows = _free_catalog_rows()
    assert 1 <= len(rows) <= FREE_CATALOG_TEASER_MAX
    assert len(rows) < HISTORICAL_PAID_CATALOG_ROWS

    html = (DOCS / "index.html").read_text(encoding="utf-8")
    lowered = html.lower()
    assert "teaser" in lowered
    assert "incomplete" in lowered
    assert "team pack" in lowered
    assert "full size a/b/c/d" in lowered


def test_published_pages_do_not_link_paid_catalog() -> None:
    for path in [*DOCS.rglob("*.html"), *DOCS.rglob("*.js")]:
        text = path.read_text(encoding="utf-8")
        assert "href=\"./4130-catalog.csv\"" not in text
        assert "href='/4130-catalog.csv'" not in text
        assert "4130-catalog.csv" not in text


def test_pack_html_uses_shared_gate_and_omits_old_unlock() -> None:
    html = (DOCS / "pack.html").read_text(encoding="utf-8")
    assert 'src="./pack.js"' in html
    assert "renderPackPage" in html
    assert "|| !cfg.paymentUrl" not in html
    assert 'params.get("k")' not in html


def test_unlock_does_not_succeed_when_payment_url_empty() -> None:
    leaked_cfg = {"paymentUrl": "", "unlockToken": "2k4130pack"}
    assert is_pack_unlocked(leaked_cfg, {"k": "2k4130pack"}) is False
    assert is_pack_unlocked({"paymentUrl": ""}, {}) is False
    assert is_pack_unlocked({}, {}) is False
    assert pack_page_state(leaked_cfg, {"k": "2k4130pack"}) == "unconfigured"
    assert _js_call("isPackUnlocked", leaked_cfg, {"k": "2k4130pack"}) is False
    assert _js_call("packPageState", leaked_cfg, {"k": "2k4130pack"}) == "unconfigured"


def test_unlock_does_not_treat_query_token_as_paywall() -> None:
    cfg = {"paymentUrl": "https://payhip.com/b/example", "unlockToken": "2k4130pack"}
    assert is_pack_unlocked(cfg, {"k": "2k4130pack"}) is False
    assert is_pack_unlocked(cfg, {"paid": "1"}) is False
    assert pack_page_state(cfg, {"paid": "1"}) == "thanks"
    assert pack_page_state(cfg, {}) == "checkout"
    assert _js_call("isPackUnlocked", cfg, {"k": "2k4130pack"}) is False
    assert _js_call("isPackUnlocked", cfg, {"paid": "1"}) is False
    assert _js_call("packPageState", cfg, {"paid": "1"}) == "thanks"
    assert _js_call("packPageState", cfg, {}) == "checkout"
