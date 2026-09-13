"""In-process 3 / client / UTC-day cap. No network."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime, timezone
from threading import Lock

from .policy import FREE_AUDITS_PER_IP_PER_DAY


class RateLimiter:
    def __init__(self, limit: int = FREE_AUDITS_PER_IP_PER_DAY) -> None:
        self.limit = limit
        self._lock = Lock()
        self._counts: dict[tuple[str, date], int] = defaultdict(int)

    def allow(self, client_id: str, when: datetime | None = None) -> tuple[bool, int]:
        stamp = when or datetime.now(timezone.utc)
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        key = (client_id or "unknown", stamp.date())
        with self._lock:
            used = self._counts[key]
            if used >= self.limit:
                return False, 0
            self._counts[key] = used + 1
            return True, self.limit - (used + 1)


DEFAULT_LIMITER = RateLimiter()
