#!/usr/bin/env python3
"""Serve the Inbound Score landing + gated audit stub. No spend by default."""

from __future__ import annotations

import argparse
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
PRODUCT = ROOT.parent
if str(PRODUCT) not in sys.path:
    sys.path.insert(0, str(PRODUCT))

from inbound_audit.render import render_audit_page
from inbound_audit.runner import run_free_audit

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class LandingHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index", "/index.html"}:
            self.path = "/index.html"
        elif parsed.path in {"/audit", "/audit.html"}:
            qs = parse_qs(parsed.query)
            if qs.get("url"):
                self._audit_response(qs)
                return
            self.path = "/audit.html"
        elif parsed.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path not in {"/audit", "/audit.html"}:
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        self._audit_response(parse_qs(raw))

    def _audit_response(self, fields: dict[str, list[str]]) -> None:
        def first(name: str) -> str:
            values = fields.get(name) or []
            return values[0] if values else ""

        client = self.client_address[0] if self.client_address else "local"
        result = run_free_audit(
            first("url"),
            first("brand"),
            first("competitors"),
            client_id=client,
        )
        body = render_audit_page(result)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        super().log_message(format, *args)


def make_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), LandingHandler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve Inbound Score landing + audit stub")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args(argv)
    server = make_server(args.host, args.port)
    host, port = server.server_address[:2]
    print(f"Inbound Score landing: http://{host}:{port}/")
    print(f"Free audit (stub):     http://{host}:{port}/audit")
    print("Live engine calls are off unless INBOUND_SCORE_LIVE=1, keys, and INBOUND_SCORE_AC0B=1")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
