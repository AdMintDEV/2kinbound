"""Free-audit runner. Default: stub. Never invents citations."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from .policy import LOCKED_ENGINE_IDS, live_calls_permitted
from .rate_limit import DEFAULT_LIMITER, RateLimiter
from .validate import AuditRequest, InvalidAuditInput, parse_audit_request


def run_free_audit(
    url: str,
    brand: str = "",
    competitors: str = "",
    *,
    client_id: str = "local",
    env: Mapping[str, str] | None = None,
    limiter: RateLimiter | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Execute one free-audit attempt.

    Live API calls happen only when live_calls_permitted(env) is true.
    This module does not invent citation rows in either branch.
    """
    stamp = now or datetime.now(timezone.utc)
    try:
        request = parse_audit_request(url, brand, competitors)
    except InvalidAuditInput as exc:
        return _payload(
            status="invalid",
            request=None,
            reason=str(exc),
            remaining=None,
            live=False,
            stamp=stamp,
        )

    gate = limiter or DEFAULT_LIMITER
    allowed, remaining = gate.allow(client_id, stamp)
    if not allowed:
        return _payload(
            status="rate_limited",
            request=request,
            reason="free audit limit is 3 per IP per day",
            remaining=0,
            live=False,
            stamp=stamp,
        )

    permitted, why = live_calls_permitted(env)
    if not permitted:
        return _payload(
            status="stub",
            request=request,
            reason=why,
            remaining=remaining,
            live=False,
            stamp=stamp,
            note=(
                "AC#0a allows this code path. Live free-audit traffic waits on "
                "AC#0b. No engine HTTP was sent. Citations stay empty."
            ),
        )

    # AC#0b + opt-in + keys: still refuse to silently invent results.
    # Real provider calls are not implemented here to prevent accidental spend.
    return _payload(
        status="live_not_implemented",
        request=request,
        reason="ac0b_live_path_not_wired_to_prevent_spend",
        remaining=remaining,
        live=True,
        stamp=stamp,
        note=(
            "Keys/opt-in/AC#0b flags are set, but this build will not call "
            "openai-web-search or perplexity-sonar until a human-approved "
            "spend review. No citations invented."
        ),
    )


def _payload(
    *,
    status: str,
    request: AuditRequest | None,
    reason: str,
    remaining: int | None,
    live: bool,
    stamp: datetime,
    note: str = "",
) -> dict[str, Any]:
    return {
        "status": status,
        "reason": reason,
        "note": note,
        "engines": list(LOCKED_ENGINE_IDS),
        "citations": [],
        "invented": False,
        "live": live,
        "ac0a": "PASS",
        "ac0b": "TODO",
        "remaining_today": remaining,
        "timestamp": stamp.isoformat(),
        "request": (
            {
                "url": request.url,
                "brand": request.brand,
                "competitors": list(request.competitors),
            }
            if request
            else None
        ),
    }
