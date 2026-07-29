#!/usr/bin/env python3
"""Static file server + POST /__log for hero diagnostics."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "assets" / "hero-video" / "session.log"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        # quieter access log; hero logs go to session.log
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        path = unquote(self.path.split("?", 1)[0])
        if path != "/__log":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            data = {"raw": raw.decode("utf-8", errors="replace")}

        ts = datetime.now(timezone.utc).isoformat()
        line = json.dumps({"server_ts": ts, **data}, ensure_ascii=False)
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()

        # also mirror to stdout for live tail
        print(line, flush=True)

        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        path = unquote(self.path.split("?", 1)[0])
        if path == "/__log":
            # dump log for agent
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            if LOG_PATH.exists():
                self.wfile.write(LOG_PATH.read_bytes())
            return
        if path == "/__log/clear":
            LOG_PATH.write_text("", encoding="utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"cleared\n")
            return
        return super().do_GET()


def main():
    LOG_PATH.write_text("", encoding="utf-8")
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"SERVING http://127.0.0.1:{PORT}/", flush=True)
    print(f"LOGFILE {LOG_PATH}", flush=True)
    print("Open the URL, hard-refresh, do ONE scroll from the top.", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye", flush=True)


if __name__ == "__main__":
    main()
