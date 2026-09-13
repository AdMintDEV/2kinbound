"""Input checks for the free-audit form. No network."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


class InvalidAuditInput(ValueError):
    pass


@dataclass(frozen=True)
class AuditRequest:
    url: str
    brand: str
    competitors: tuple[str, ...]


def _http_url(raw: str, *, field: str) -> str:
    text = (raw or "").strip()
    if not text:
        raise InvalidAuditInput(f"{field} is required")
    parsed = urlparse(text)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise InvalidAuditInput(f"{field} must be an http(s) URL")
    if parsed.username or parsed.password:
        raise InvalidAuditInput(f"{field} must not include credentials")
    return text


def parse_audit_request(
    url: str,
    brand: str = "",
    competitors: str = "",
    *,
    max_competitors: int = 2,
) -> AuditRequest:
    brand_url = _http_url(url, field="url")
    extra: list[str] = []
    for chunk in (competitors or "").replace(",", " ").split():
        extra.append(_http_url(chunk, field="competitors"))
        if len(extra) > max_competitors:
            raise InvalidAuditInput("at most 2 competitor URLs")
    return AuditRequest(
        url=brand_url,
        brand=(brand or "").strip()[:80],
        competitors=tuple(extra),
    )
