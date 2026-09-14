#!/usr/bin/env python3
"""Build a private, rotated 4130 Team Pack catalog via TubeCheck geometry.

Outputs (gitignored) under pack/private/:
  - 4130-team-pack-catalog.csv
  - PACK_NOTES.md
  - 4130-team-pack.zip

Do not copy git-history catalogs. Do not commit pack/private/.
"""

from __future__ import annotations

import csv
import io
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from tubecheck import evaluate, inch  # noqa: E402

PACK_VERSION = "2026.09-r1"
OUTPUT_DIR = ROOT / "pack" / "private"
CATALOG_NAME = "4130-team-pack-catalog.csv"
NOTES_NAME = "PACK_NOTES.md"
ZIP_NAME = "4130-team-pack.zip"

CSV_FIELDNAMES = [
    "shape",
    "od_in",
    "wall_in",
    "od_mm",
    "wall_mm",
    "area_mm2",
    "I_mm4",
    "lb_ft",
    "kg_m",
    "A",
    "B",
    "C",
    "D",
    "meets",
]

# Common 4130 stock for FSAE frames. Not the historically public 19-row list.
ROUND_STOCK: tuple[tuple[float, float], ...] = (
    (0.625, 0.035),
    (0.625, 0.049),
    (0.625, 0.065),
    (0.750, 0.035),
    (0.750, 0.049),
    (0.750, 0.058),
    (0.750, 0.065),
    (0.750, 0.083),
    (0.875, 0.049),
    (0.875, 0.065),
    (0.875, 0.083),
    (1.000, 0.035),
    (1.000, 0.049),
    (1.000, 0.058),
    (1.000, 0.065),
    (1.000, 0.083),
    (1.000, 0.095),
    (1.000, 0.120),
    (1.000, 0.134),
    (1.125, 0.049),
    (1.125, 0.065),
    (1.125, 0.083),
    (1.125, 0.095),
    (1.250, 0.035),
    (1.250, 0.049),
    (1.250, 0.065),
    (1.250, 0.083),
    (1.250, 0.095),
    (1.250, 0.120),
    (1.375, 0.049),
    (1.375, 0.065),
    (1.375, 0.083),
    (1.375, 0.095),
    (1.500, 0.049),
    (1.500, 0.065),
    (1.500, 0.083),
    (1.500, 0.095),
    (1.500, 0.120),
    (1.625, 0.049),
    (1.625, 0.065),
    (1.625, 0.095),
    (1.750, 0.049),
    (1.750, 0.065),
    (1.750, 0.095),
    (1.750, 0.120),
    (2.000, 0.049),
    (2.000, 0.065),
    (2.000, 0.083),
    (2.000, 0.095),
    (2.000, 0.120),
)

SQUARE_STOCK: tuple[tuple[float, float], ...] = (
    (0.750, 0.049),
    (0.750, 0.065),
    (1.000, 0.049),
    (1.000, 0.065),
    (1.000, 0.083),
    (1.000, 0.095),
    (1.000, 0.120),
    (1.250, 0.049),
    (1.250, 0.065),
    (1.250, 0.083),
    (1.250, 0.095),
    (1.500, 0.065),
    (1.500, 0.095),
    (1.500, 0.120),
    (2.000, 0.065),
    (2.000, 0.095),
)


def _yn(passed: bool) -> str:
    return "Y" if passed else "n"


def _fmt_in(value: float) -> str:
    return f"{value:.3f}"


def catalog_header_comments(generated_utc: str, row_count: int) -> str:
    return (
        f"# 4130 Team Pack catalog\n"
        f"# pack_version: {PACK_VERSION}\n"
        f"# generated_utc: {generated_utc}\n"
        f"# rows: {row_count}\n"
        f"# geometry: TubeCheck evaluate() — unofficial helper, not SAE, not SES\n"
        f"# pack_notes: see PACK_NOTES.md in this folder / zip\n"
        f"# do_not_commit: attach only via Payhip/Stripe from pack/private/\n"
    )


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for shape, stock in (("round", ROUND_STOCK), ("square", SQUARE_STOCK)):
        for od_in, wall_in in stock:
            result = evaluate(shape, inch(od_in), inch(wall_in))
            meets = [name for name in ("A", "B", "C", "D") if result.sizes[name]["pass"]]
            rows.append(
                {
                    "shape": result.shape,
                    "od_in": _fmt_in(od_in),
                    "wall_in": _fmt_in(wall_in),
                    "od_mm": f"{result.od_mm:.4f}",
                    "wall_mm": f"{result.wall_mm:.4f}",
                    "area_mm2": f"{result.area_mm2:.4f}",
                    "I_mm4": f"{result.inertia_mm4:.2f}",
                    "lb_ft": f"{result.mass_lb_ft:.4f}",
                    "kg_m": f"{result.mass_kg_m:.4f}",
                    "A": _yn(bool(result.sizes["A"]["pass"])),
                    "B": _yn(bool(result.sizes["B"]["pass"])),
                    "C": _yn(bool(result.sizes["C"]["pass"])),
                    "D": _yn(bool(result.sizes["D"]["pass"])),
                    "meets": ",".join(meets) if meets else "none",
                }
            )
    return rows


def render_csv(rows: list[dict[str, str]], generated_utc: str) -> str:
    buf = io.StringIO()
    buf.write(catalog_header_comments(generated_utc, len(rows)))
    writer = csv.DictWriter(buf, fieldnames=CSV_FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def render_notes(generated_utc: str, row_count: int) -> str:
    return (
        f"# 4130 Team Pack — notes\n"
        f"\n"
        f"**Pack version:** {PACK_VERSION}  \n"
        f"**Generated (UTC):** {generated_utc}  \n"
        f"**Rows:** {row_count} (Size A/B/C/D map via TubeCheck geometry)\n"
        f"\n"
        f"## Disclaimer\n"
        f"\n"
        f"This catalog is an **unofficial helper**. It is **not SAE**, **not a substitute "
        f"for the official SES**, and **not** the Formula SAE Rules. Values are computed "
        f"from the same TubeCheck geometry as the free checker (area, second moment, "
        f"mass, Size A/B/C/D pass/fail). Inch stock vs millimetre rule tables can "
        f"disagree by tenths of a millimetre — verify against the current published "
        f"rules and your team's SES before you cut or submit.\n"
        f"\n"
        f"## How to use with the free checker\n"
        f"\n"
        f"1. Open the free TubeCheck page (GitHub Pages site for this project).\n"
        f"2. Enter a catalog row's **shape**, **OD (in)**, and **wall (in)**.\n"
        f"3. Compare the checker's Size A/B/C/D result to the `A`,`B`,`C`,`D` / `meets` columns.\n"
        f"4. Use the free nest tool for stick cuts. This CSV is a size map, not a nest plan.\n"
        f"\n"
        f"## Files in this pack\n"
        f"\n"
        f"- `{CATALOG_NAME}` — full Size A/B/C/D 4130 stock map (generated, not copied from git history)\n"
        f"- `{NOTES_NAME}` — this file\n"
        f"\n"
        f"Do **not** upload any catalog recovered from an old git SHA or raw GitHub URL. "
        f"Do **not** commit these files to a public repository, gist, or Pages tree.\n"
    )


def write_bundle(output_dir: Path | None = None) -> dict[str, Path]:
    dest = output_dir or OUTPUT_DIR
    dest.mkdir(parents=True, exist_ok=True)
    generated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows = build_rows()
    csv_text = render_csv(rows, generated_utc)
    notes_text = render_notes(generated_utc, len(rows))

    catalog_path = dest / CATALOG_NAME
    notes_path = dest / NOTES_NAME
    zip_path = dest / ZIP_NAME
    catalog_path.write_text(csv_text, encoding="utf-8")
    notes_path.write_text(notes_text, encoding="utf-8")

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(CATALOG_NAME, csv_text)
        zf.writestr(NOTES_NAME, notes_text)

    return {"catalog": catalog_path, "notes": notes_path, "zip": zip_path}


def main() -> int:
    paths = write_bundle()
    for label, path in paths.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
