"""Team Pack must not leak on the GitHub Pages publish root."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tubecheck.pack_gate import is_pack_unlocked, pack_page_state

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


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


def test_paid_catalog_not_in_pages_publish_root() -> None:
    assert not (DOCS / "4130-catalog.csv").exists()
    assert list(DOCS.rglob("*.csv")) == []


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
