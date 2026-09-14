"""T13: generator exists; outputs stay gitignored; public tree has no full catalog."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import subprocess
from pathlib import Path

from tubecheck import evaluate, inch

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_team_pack.py"

# SHA-256 of the historically public docs/4130-catalog.csv (git SHA 3871f04).
# Merchant file must be freshly generated and must not match this blob.
HISTORICAL_CATALOG_SHA256 = (
    "316a12c842aa06c7b5b0dff09982cd077f8a2403bc40e3ec06ecbd1b2e3bfd1f"
)
HISTORICAL_PAID_CATALOG_ROWS = 19
PRIVATE_OUTPUTS = (
    "pack/private/4130-team-pack-catalog.csv",
    "pack/private/PACK_NOTES.md",
    "pack/private/4130-team-pack.zip",
)


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_team_pack", GENERATOR)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tracked_paths() -> list[str]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [p.decode() for p in raw.split(b"\0") if p]


def test_generator_script_is_tracked_and_private_dir_is_ignored() -> None:
    assert GENERATOR.is_file()
    tracked = _tracked_paths()
    assert "scripts/generate_team_pack.py" in tracked

    for rel in PRIVATE_OUTPUTS:
        result = subprocess.run(
            ["git", "check-ignore", "-v", rel],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        assert "pack/private/" in result.stdout
        assert rel in result.stdout


def test_public_tree_has_no_full_or_team_pack_catalog() -> None:
    tracked = _tracked_paths()
    banned = {
        "4130-catalog.csv",
        "4130-team-pack-catalog.csv",
        "4130-team-pack.zip",
        "PACK_NOTES.md",
    }
    hits = [rel for rel in tracked if Path(rel).name in banned]
    assert hits == [], f"paid pack files tracked: {hits}"
    assert not any(rel.startswith("pack/private/") for rel in tracked)


def test_generator_writes_only_pack_private_paths() -> None:
    gen = _load_generator()
    assert gen.OUTPUT_DIR == ROOT / "pack" / "private"
    assert gen.CATALOG_NAME == "4130-team-pack-catalog.csv"
    assert gen.NOTES_NAME == "PACK_NOTES.md"
    assert gen.ZIP_NAME == "4130-team-pack.zip"


def test_generator_builds_full_map_via_tubecheck_not_historical_copy(tmp_path: Path) -> None:
    gen = _load_generator()
    paths = gen.write_bundle(tmp_path)
    csv_text = paths["catalog"].read_text(encoding="utf-8")
    notes = paths["notes"].read_text(encoding="utf-8")
    digest = hashlib.sha256(csv_text.encode("utf-8")).hexdigest()

    assert digest != HISTORICAL_CATALOG_SHA256
    assert f"pack_version: {gen.PACK_VERSION}" in csv_text
    assert "generated_utc:" in csv_text
    assert "not SAE" in notes
    assert "not a substitute" in notes.lower() or "not a substitute" in notes
    assert "SES" in notes
    assert "free" in notes.lower()
    assert paths["zip"].is_file() and paths["zip"].stat().st_size > 0

    data_lines = [line for line in csv_text.splitlines() if line and not line.startswith("#")]
    reader = csv.DictReader(io.StringIO("\n".join(data_lines)))
    rows = list(reader)
    assert len(rows) > HISTORICAL_PAID_CATALOG_ROWS
    assert {"A", "B", "C", "D"}.issubset(reader.fieldnames or [])

    seen_pass = {name: False for name in ("A", "B", "C", "D")}
    for row in rows:
        result = evaluate(row["shape"], inch(float(row["od_in"])), inch(float(row["wall_in"])))
        for name in ("A", "B", "C", "D"):
            expected = "Y" if result.sizes[name]["pass"] else "n"
            assert row[name] == expected
            if expected == "Y":
                seen_pass[name] = True
    assert all(seen_pass.values()), f"catalog missing a Size class: {seen_pass}"
