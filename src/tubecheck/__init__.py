"""FSAE 2026 F.3.4 steel tube properties. Unofficial helper — not SAE or SES."""

from __future__ import annotations

import math
from dataclasses import dataclass

# Published Formula SAE Rules 2026 F.3.4.1 minima (mm / mm^4 / mm^2).
SIZES: dict[str, dict[str, float]] = {
    "A": {"I": 11320.0, "area": 173.0, "od": 25.0, "wall": 2.0},
    "B": {"I": 8509.0, "area": 114.0, "od": 25.0, "wall": 1.2},
    "C": {"I": 6695.0, "area": 91.0, "od": 25.0, "wall": 1.2},
    "D": {"I": 18015.0, "area": 126.0, "od": 35.0, "wall": 1.2},
}

APPLICATIONS: tuple[tuple[str, str, str], ...] = (
    ("Front Bulkhead", "B", "Aluminum allowed"),
    ("Front Bulkhead Support", "C", "Aluminum allowed"),
    ("Front Hoop", "A", "Aluminum allowed"),
    ("Front Hoop Bracing", "B", "Aluminum allowed"),
    ("Side Impact Structure", "B", "Aluminum allowed"),
    ("Bent / Multi Upper Side Impact Member", "D", "Aluminum allowed"),
    ("Main Hoop", "A", "Steel only"),
    ("Main Hoop Bracing", "B", "Steel only"),
    ("Main Hoop Bracing Supports", "C", "Aluminum allowed"),
    ("Driver Restraint Harness Attachment", "B", "Aluminum allowed"),
    ("Shoulder Harness Mounting Bar", "A", "Steel only"),
    ("Shoulder Harness Mounting Bar Bracing", "C", "Aluminum allowed"),
    ("Battery Pack Mounting and Protection", "B", "Aluminum allowed"),
    ("Component Protection", "C", "Aluminum allowed"),
    ("Structural Tubing", "C", "Aluminum allowed"),
)

STEEL_LB_IN3 = 0.2836
MM_PER_IN = 25.4


@dataclass(frozen=True)
class TubeResult:
    shape: str
    od_mm: float
    wall_mm: float
    id_mm: float
    area_mm2: float
    inertia_mm4: float
    mass_lb_ft: float
    mass_kg_m: float
    sizes: dict[str, dict[str, bool | str]]
    min_od_wall_warning: bool


def _round_props(od_mm: float, wall_mm: float) -> tuple[float, float, float]:
    inner = od_mm - 2.0 * wall_mm
    if inner < 0:
        raise ValueError("wall thicker than diameter")
    area = math.pi / 4.0 * (od_mm**2 - inner**2)
    inertia = math.pi / 64.0 * (od_mm**4 - inner**4)
    return inner, area, inertia


def _square_props(side_mm: float, wall_mm: float) -> tuple[float, float, float]:
    inner = side_mm - 2.0 * wall_mm
    if inner < 0:
        raise ValueError("wall thicker than side")
    area = side_mm**2 - inner**2
    inertia = (side_mm**4 - inner**4) / 12.0
    return inner, area, inertia


def _mass(area_mm2: float) -> tuple[float, float]:
    area_in2 = area_mm2 / (MM_PER_IN**2)
    lb_ft = area_in2 * 12.0 * STEEL_LB_IN3
    kg_m = lb_ft * 1.48816
    return lb_ft, kg_m


def evaluate(shape: str, od_mm: float, wall_mm: float) -> TubeResult:
    if od_mm <= 0 or wall_mm <= 0:
        raise ValueError("dimensions must be positive")
    shape = shape.lower()
    if shape in {"round", "circle", "od"}:
        inner, area, inertia = _round_props(od_mm, wall_mm)
        kind = "round"
    elif shape in {"square", "box"}:
        inner, area, inertia = _square_props(od_mm, wall_mm)
        kind = "square"
    else:
        raise ValueError("shape must be round or square")

    sizes: dict[str, dict[str, bool | str]] = {}
    for name, req in SIZES.items():
        checks = {
            "I": inertia + 1e-9 >= req["I"],
            "area": area + 1e-9 >= req["area"],
            "od": od_mm + 1e-9 >= req["od"],
            "wall": wall_mm + 1e-9 >= req["wall"],
        }
        sizes[name] = {
            **checks,
            "pass": all(checks.values()),
        }

    min_pair = abs(od_mm - 25.0) < 0.05 and wall_mm <= 2.01
    lb_ft, kg_m = _mass(area)
    return TubeResult(
        shape=kind,
        od_mm=od_mm,
        wall_mm=wall_mm,
        id_mm=inner,
        area_mm2=area,
        inertia_mm4=inertia,
        mass_lb_ft=lb_ft,
        mass_kg_m=kg_m,
        sizes=sizes,
        min_od_wall_warning=min_pair,
    )


def inch(value: float) -> float:
    return value * MM_PER_IN
