"""HTML for the audit result page. No engine calls."""

from __future__ import annotations

from html import escape
from typing import Any


def render_audit_page(result: dict[str, Any]) -> bytes:
    req = result.get("request") or {}
    url = escape(str(req.get("url") or ""))
    brand = escape(str(req.get("brand") or ""))
    status = escape(str(result.get("status") or ""))
    reason = escape(str(result.get("reason") or ""))
    note = escape(str(result.get("note") or ""))
    engines = ", ".join(escape(e) for e in result.get("engines") or [])
    remaining = result.get("remaining_today")
    rem = "—" if remaining is None else str(remaining)
    body = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Free audit — Inbound Score</title>
    <link rel="stylesheet" href="/styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="wrap">
        <a class="brand" href="/">Inbound Score</a>
        <nav aria-label="Primary"><a href="/#audit">Free audit</a></nav>
      </div>
    </header>
    <main class="wrap section">
      <p class="eyebrow">AC#2 code path · live traffic waits on AC#0b</p>
      <h1>Audit result ({status})</h1>
      <article class="panel">
        <p><strong>Brand URL:</strong> {url or "—"}</p>
        <p><strong>Brand name:</strong> {brand or "—"}</p>
        <p><strong>Reason:</strong> {reason}</p>
        <p>{note}</p>
        <p class="hint">Engines locked for later live use: {engines}. Citations returned: none (not invented). Remaining free attempts today: {rem}.</p>
        <div class="actions">
          <a class="button" href="/#audit">Back to the form</a>
          <a class="button secondary" href="/">Home</a>
        </div>
      </article>
    </main>
  </body>
</html>
"""
    return body.encode("utf-8")
