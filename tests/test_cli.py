from pathlib import Path

from forge.cli import main


def test_cli_pipeline_list_and_show(tmp_path: Path, capsys) -> None:
    db = tmp_path / "forge.db"
    sample = Path("data/sample_records.json")
    assert main(["--db", str(db), "pipeline", str(sample)]) == 0
    assert main(["--db", str(db), "list"]) == 0
    listed = capsys.readouterr().out
    assert "tube-chassis" in listed
    assert "thin-data" in listed

    assert main(["--db", str(db), "show", "thin-data"]) == 0
    shown = capsys.readouterr().out
    assert "Unnamed local services idea" in shown
    assert '"adjusted_score": 0.0' in shown or '"adjusted_score": 0' in shown


def test_cli_unknown_record(tmp_path: Path, capsys) -> None:
    db = tmp_path / "forge.db"
    assert main(["--db", str(db), "show", "missing"]) == 1
    assert "unknown record" in capsys.readouterr().err


def test_cli_db_flag_after_subcommand(tmp_path: Path, capsys) -> None:
    db = tmp_path / "forge.db"
    sample = Path("data/sample_records.json")
    assert main(["pipeline", str(sample), "--db", str(db)]) == 0
    assert "ingested=4" in capsys.readouterr().out
