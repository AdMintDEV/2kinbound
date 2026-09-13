from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def test_full_catalog_not_in_pages_root() -> None:
    assert not (DOCS / "4130-catalog.csv").exists()


def test_pages_workflow_publishes_docs_only() -> None:
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text()
    assert "path: docs" in workflow
    assert "pack_assets" not in workflow


def test_public_docs_do_not_link_paid_catalog() -> None:
    for path in DOCS.rglob("*"):
        if path.is_file() and path.suffix in {".html", ".js", ".css", ".csv"}:
            text = path.read_text()
            assert "4130-catalog.csv" not in text
            assert "unlockToken" not in text
            assert "2k4130pack" not in text


def test_empty_payment_url_does_not_unlock_pack() -> None:
    app = (DOCS / "app.js").read_text()
    assert 'btn.href = "./pack.html"' not in app
    assert "Checkout coming soon" in app
    pack = (DOCS / "pack.html").read_text()
    assert "does not host or unlock" in pack
    assert "<a href=" not in pack or "./4130-catalog.csv" not in pack
