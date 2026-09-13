from pathlib import Path

from forge.ingest import load_records, parse_records


def test_parse_list_and_wrapper() -> None:
    records, errors = parse_records([{"title": "One"}, {"title": "Two"}])
    assert len(records) == 2
    assert errors == []

    wrapped, wrapped_errors = parse_records({"records": [{"title": "Three"}]})
    assert len(wrapped) == 1
    assert wrapped_errors == []


def test_parse_rejects_empty_and_invalid() -> None:
    assert parse_records(None)[1]
    assert parse_records([])[1] == ["no research records found"]
    records, errors = parse_records([{"title": ""}, {"title": "Ok"}])
    assert len(records) == 1
    assert errors


def test_load_file_errors(tmp_path: Path) -> None:
    missing = tmp_path / "nope.json"
    records, errors = load_records(missing)
    assert records == []
    assert "file not found" in errors[0]

    empty = tmp_path / "empty.json"
    empty.write_text(" \n", encoding="utf-8")
    _, empty_errors = load_records(empty)
    assert empty_errors == ["file is empty"]

    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    _, bad_errors = load_records(bad)
    assert "invalid JSON" in bad_errors[0]


def test_load_sample_file() -> None:
    records, errors = load_records(Path("data/sample_records.json"))
    assert errors == []
    assert len(records) == 4
    assert {record.id for record in records} >= {"tube-chassis", "thin-data"}
