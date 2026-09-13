#!/usr/bin/env python3
"""Serve the Inbound Score landing (stdlib only). No engine calls."""

from __future__ import annotations

import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
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
            self.path = "/audit.html"
        elif parsed.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        return super().do_GET()

    def log_message(self, format: str, *args: object) -> None:
        super().log_message(format, *args)


def make_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), LandingHandler)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve Inbound Score AC#1 landing")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args(argv)
    server = make_server(args.host, args.port)
    host, port = server.server_address[:2]
    print(f"Inbound Score landing: http://{host}:{port}/")
    print(f"Free audit stub:      http://{host}:{port}/audit")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
