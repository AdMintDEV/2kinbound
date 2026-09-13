"""AC#1 landing copy and routes. No network to third parties."""

from __future__ import annotations

import sys
import threading
from pathlib import Path
from urllib.request import urlopen

LANDING_DIR = Path(__file__).resolve().parents[1] / "product" / "landing"
sys.path.insert(0, str(LANDING_DIR))

from serve import make_server  # noqa: E402

INDEX = (LANDING_DIR / "index.html").read_text(encoding="utf-8")
AUDIT = (LANDING_DIR / "audit.html").read_text(encoding="utf-8")
CSS = (LANDING_DIR / "styles.css").read_text(encoding="utf-8")
ALL_TEXT = "\n".join(
    path.read_text(encoding="utf-8") for path in LANDING_DIR.glob("*") if path.suffix in {".html", ".css", ".js", ".py", ".md"}
)


def test_index_has_value_prop_icp_pricing_and_cta() -> None:
    lower = INDEX.lower()
    assert "Inbound Score" in INDEX
    assert "B2B SaaS" in INDEX
    assert "50" in INDEX
    assert "AI-visibility" in INDEX or "AI visibility" in INDEX
    assert "$29" in INDEX
    assert "free audit" in lower
    assert 'id="audit"' in INDEX
    assert 'action="/audit"' in INDEX
    assert 'name="url"' in INDEX
    assert 'href="#audit"' in INDEX
    assert 'href="#pricing"' in INDEX
    assert 'href="#icp"' in INDEX


def test_starter_limits_match_ac0_not_invented_metrics() -> None:
    assert "2 on-demand" in INDEX
    assert "4 scheduled" in INDEX
    assert "2 competitors" in INDEX
    assert "3 audits per IP" in INDEX or "3 / IP" in INDEX


def test_no_fake_social_proof_or_spam_features() -> None:
    blob = ALL_TEXT.lower()
    banned = (
        "testimonial",
        "as featured",
        "loved by",
        "trusted by",
        "5000 teams",
        "10,000",
        "linkedin automation",
        "reddit automation",
        "outreach sequence",
    )
    for phrase in banned:
        assert phrase not in blob, phrase


def test_no_engine_api_calls_in_landing() -> None:
    blob = ALL_TEXT
    assert "api.openai.com" not in blob
    assert "api.perplexity.ai" not in blob
    assert "openai-web-search" not in blob
    assert "perplexity-sonar" not in blob
    assert "fetch(" not in blob
    assert "XMLHttpRequest" not in blob


def test_does_not_claim_measured_cogs() -> None:
    blob = ALL_TEXT.lower()
    assert "measured cogs" not in blob
    assert "measured $/run" not in blob


def test_audit_stub_says_not_live() -> None:
    lower = AUDIT.lower()
    assert "not live" in lower
    assert "not</strong> calling" in AUDIT or "not calling" in lower
    assert "invent" in lower
    assert "$29" in AUDIT


def test_server_serves_home_audit_and_health() -> None:
    server = make_server("127.0.0.1", 0)
    host, port = server.server_address[:2]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://{host}:{port}"
        home = urlopen(f"{base}/", timeout=3).read().decode("utf-8")
        audit = urlopen(f"{base}/audit?url=https://www.example.com", timeout=3).read().decode("utf-8")
        css = urlopen(f"{base}/styles.css", timeout=3).read().decode("utf-8")
        health = urlopen(f"{base}/healthz", timeout=3).read().decode("utf-8")
        assert "Inbound Score" in home
        assert "$29" in home
        assert "Audit runner is not live" in audit
        assert ":root" in css
        assert health.strip() == "ok"
    finally:
        server.shutdown()
        server.server_close()
