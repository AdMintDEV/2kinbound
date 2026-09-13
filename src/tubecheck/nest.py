"""Greedy first-fit-decreasing nest onto stock sticks."""

from __future__ import annotations


def nest(
    lengths: list[float],
    stock: float,
    kerf: float = 0.06,
    end_trim: float = 0.25,
) -> dict:
    usable = stock - 2.0 * end_trim
    if usable <= 0:
        raise ValueError("stock too short for end trim")
    if any(length <= 0 for length in lengths):
        raise ValueError("cut lengths must be positive")
    pieces = sorted(lengths, reverse=True)
    if any(length > usable for length in pieces):
        too_long = [length for length in pieces if length > usable]
        raise ValueError(f"piece longer than usable stock: {too_long}")

    sticks: list[list[float]] = []
    remainders: list[float] = []
    for length in pieces:
        placed = False
        for index, remaining in enumerate(remainders):
            extra = kerf if sticks[index] else 0.0
            if length + extra <= remaining + 1e-9:
                sticks[index].append(length)
                remainders[index] -= length + extra
                placed = True
                break
        if not placed:
            sticks.append([length])
            remainders.append(usable - length)

    used = sum(sum(stick) for stick in sticks) + kerf * sum(max(0, len(stick) - 1) for stick in sticks)
    return {
        "stock": stock,
        "usable": usable,
        "kerf": kerf,
        "end_trim": end_trim,
        "sticks": sticks,
        "remainders": remainders,
        "stick_count": len(sticks),
        "total_cut": sum(pieces),
        "waste": sum(remainders),
        "used": used,
    }
