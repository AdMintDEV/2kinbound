"""Command-line interface for the Forge pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from forge.pipeline import Pipeline
from forge.storage import DEFAULT_DB_PATH, Store


def _pipeline(db: str) -> Pipeline:
    return Pipeline(Store(db))


def cmd_ingest(args: argparse.Namespace) -> int:
    result = _pipeline(args.db).run_file(args.path)
    print(f"ingested={result.ingested} scored={result.scored} skipped={result.skipped}")
    if result.errors:
        for error in result.errors:
            print(f"error: {error}", file=sys.stderr)
        return 1 if result.ingested == 0 else 0
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    result = _pipeline(args.db).rescore_all()
    print(f"rescored={result.scored}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    store = Store(args.db)
    pairs = store.scored_pairs()
    if not pairs:
        print("no scored opportunities")
        return 0
    print(f"{'ID':<14} {'ADJ':>6} {'RAW':>6} {'CONF':>6} {'BAND':<8} TITLE")
    for record, score in pairs:
        print(
            f"{record.id:<14} {score.adjusted_score:6.1f} {score.raw_score:6.1f} "
            f"{score.confidence:6.1f} {score.rank_band():<8} {record.title}"
        )
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    store = Store(args.db)
    record = store.get_record(args.record_id)
    score = store.get_score(args.record_id)
    if record is None:
        print(f"unknown record: {args.record_id}", file=sys.stderr)
        return 1
    payload = {
        "record": json.loads(record.model_dump_json()),
        "score": json.loads(score.model_dump_json()) if score else None,
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_pipeline(args: argparse.Namespace) -> int:
    return cmd_ingest(args)


def cmd_serve(args: argparse.Namespace) -> int:
    import os

    import uvicorn

    os.environ["FORGE_DB"] = args.db
    from forge.api import create_app

    uvicorn.run(create_app(args.db), host=args.host, port=args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--db", default=str(DEFAULT_DB_PATH), help="SQLite database path")

    parser = argparse.ArgumentParser(
        prog="forge",
        description="Opportunity scoring pipeline",
        parents=[parent],
    )
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Ingest and score a JSON research file", parents=[parent])
    ingest.add_argument("path", type=Path)
    ingest.set_defaults(func=cmd_ingest)

    pipeline = sub.add_parser(
        "pipeline",
        help="Run the full ingest → score → store pipeline",
        parents=[parent],
    )
    pipeline.add_argument("path", type=Path)
    pipeline.set_defaults(func=cmd_pipeline)

    score = sub.add_parser("score", help="Rescore every stored research record", parents=[parent])
    score.set_defaults(func=cmd_score)

    listing = sub.add_parser("list", help="List scored opportunities", parents=[parent])
    listing.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="Show one record and its score as JSON", parents=[parent])
    show.add_argument("record_id")
    show.set_defaults(func=cmd_show)

    serve = sub.add_parser("serve", help="Run the local API and dashboard", parents=[parent])
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.set_defaults(func=cmd_serve)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
