"""AC#2 free-audit code path. No third-party network."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from inbound_audit.policy import LOCKED_ENGINE_IDS, live_calls_permitted
from inbound_audit.rate_limit import RateLimiter
from inbound_audit.runner import run_free_audit
from inbound_audit.validate import InvalidAuditInput, parse_audit_request


def test_locked_engines_are_exactly_ac0() -> None:
    assert LOCKED_ENGINE_IDS == ("openai-web-search", "perplexity-sonar")


def test_live_gate_requires_opt_in_keys_and_ac0b() -> None:
    assert live_calls_permitted({}) == (False, "opt_in_missing")
    assert live_calls_permitted({"INBOUND_SCORE_LIVE": "1"}) == (False, "keys_missing")
    assert live_calls_permitted(
        {
            "INBOUND_SCORE_LIVE": "1",
            "OPENAI_API_KEY": "sk-test",
            "PERPLEXITY_API_KEY": "pplx-test",
        }
    ) == (False, "ac0b_not_cleared")
    ok, why = live_calls_permitted(
        {
            "INBOUND_SCORE_LIVE": "1",
            "OPENAI_API_KEY": "sk-test",
            "PERPLEXITY_API_KEY": "pplx-test",
            "INBOUND_SCORE_AC0B": "1",
        }
    )
    assert ok is True
    assert why == "permitted"


def test_invalid_url_rejected() -> None:
    with pytest.raises(InvalidAuditInput):
        parse_audit_request("javascript:alert(1)")
    with pytest.raises(InvalidAuditInput):
        parse_audit_request("")
    out = run_free_audit("not-a-url")
    assert out["status"] == "invalid"
    assert out["citations"] == []
    assert out["invented"] is False
    assert out["live"] is False


def test_default_run_is_stub_with_empty_citations() -> None:
    limiter = RateLimiter()
    result = run_free_audit(
        "https://www.example.com",
        "Northwind",
        "https://competitor.example",
        client_id="t1",
        env={},
        limiter=limiter,
        now=datetime(2026, 9, 13, tzinfo=timezone.utc),
    )
    assert result["status"] == "stub"
    assert result["reason"] == "opt_in_missing"
    assert result["citations"] == []
    assert result["engines"] == list(LOCKED_ENGINE_IDS)
    assert result["ac0b"] == "TODO"
    assert result["live"] is False
    assert result["request"]["url"] == "https://www.example.com"


def test_rate_limit_fourth_request() -> None:
    limiter = RateLimiter()
    now = datetime(2026, 9, 13, 12, tzinfo=timezone.utc)
    for _ in range(3):
        assert (
            run_free_audit(
                "https://www.example.com",
                client_id="ip-1",
                env={},
                limiter=limiter,
                now=now,
            )["status"]
            == "stub"
        )
    blocked = run_free_audit(
        "https://www.example.com",
        client_id="ip-1",
        env={},
        limiter=limiter,
        now=now,
    )
    assert blocked["status"] == "rate_limited"
    assert blocked["citations"] == []


def test_keys_without_ac0b_still_stub_no_spend() -> None:
    result = run_free_audit(
        "https://www.example.com",
        env={
            "INBOUND_SCORE_LIVE": "1",
            "OPENAI_API_KEY": "sk-test",
            "PERPLEXITY_API_KEY": "pplx-test",
        },
        limiter=RateLimiter(),
    )
    assert result["status"] == "stub"
    assert result["reason"] == "ac0b_not_cleared"
    assert result["citations"] == []
    assert result["live"] is False


def test_even_full_flags_do_not_invent_or_call() -> None:
    result = run_free_audit(
        "https://www.example.com",
        env={
            "INBOUND_SCORE_LIVE": "1",
            "OPENAI_API_KEY": "sk-test",
            "PERPLEXITY_API_KEY": "pplx-test",
            "INBOUND_SCORE_AC0B": "1",
        },
        limiter=RateLimiter(),
    )
    assert result["status"] == "live_not_implemented"
    assert result["citations"] == []
    assert result["invented"] is False
