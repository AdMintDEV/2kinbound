"""Gates for AC#2 live spend. Default is stub — no API calls."""

from __future__ import annotations

import os
from typing import Mapping

from cogs_spike.engines import ALLOWED_ENGINES

LOCKED_ENGINE_IDS: tuple[str, ...] = tuple(e.engine_id for e in ALLOWED_ENGINES)
assert LOCKED_ENGINE_IDS == ("openai-web-search", "perplexity-sonar")

LIVE_OPT_IN = "INBOUND_SCORE_LIVE"
AC0B_CLEARED = "INBOUND_SCORE_AC0B"
OPENAI_KEY = "OPENAI_API_KEY"
PERPLEXITY_KEY = "PERPLEXITY_API_KEY"

FREE_AUDITS_PER_IP_PER_DAY = 3


def live_calls_permitted(env: Mapping[str, str] | None = None) -> tuple[bool, str]:
    """Return (ok, reason). Production traffic requires AC#0b explicitly."""
    source = env if env is not None else os.environ
    if source.get(LIVE_OPT_IN) != "1":
        return False, "opt_in_missing"
    if not source.get(OPENAI_KEY) or not source.get(PERPLEXITY_KEY):
        return False, "keys_missing"
    if source.get(AC0B_CLEARED) != "1":
        return False, "ac0b_not_cleared"
    return True, "permitted"
