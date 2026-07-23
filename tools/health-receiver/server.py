#!/usr/bin/env python3
"""health-receiver — recibe los POST de las automations REST API de
Health Auto Export y los guarda en vault/Raw/health/. Corre en la Mac,
no necesita que la app del iPhone esté abierta (Apple solo exige que
el iPhone se haya desbloqueado en algún momento).

Config en ~/.hestia/health-receiver.env:
    API_KEY=...
    PORT=9001
"""

import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HESTIA_DIR = Path.home() / ".hestia"
ENV_FILE = HESTIA_DIR / "health-receiver.env"
LOG_FILE = HESTIA_DIR / "health-receiver.log"


def _vault_root() -> Path:
    """VAULT_ROOT desde ~/.hestia/vault-root.env (lo escribe el /setup); default sensato."""
    f = HESTIA_DIR / "vault-root.env"
    if f.exists():
        for raw in f.read_text().splitlines():
            line = raw.strip()
            if line.startswith("VAULT_ROOT="):
                return Path(line.split("=", 1)[1].strip()).expanduser()
    return Path.home() / "second-brain"


HEALTH_DIR = _vault_root() / "vault" / "Raw" / "health"


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with LOG_FILE.open("a") as f:
        f.write(line + "\n")


def load_env() -> dict:
    if not ENV_FILE.exists():
        raise SystemExit(f"Falta {ENV_FILE} — ver tools/health-receiver/SETUP.md")
    env = {}
    for raw in ENV_FILE.read_text().splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    if not env.get("API_KEY"):
        raise SystemExit(f"Falta API_KEY en {ENV_FILE}")
    return env


ENV = load_env()
API_KEY = ENV["API_KEY"]
PORT = int(ENV.get("PORT", "9001"))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # usamos log() propio, no el default a stderr

    def do_POST(self):
        if self.headers.get("X-API-Key") != API_KEY:
            self.send_response(401)
            self.end_headers()
            log(f"401 rechazado desde {self.client_address[0]}")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""

        name = self.headers.get("automation-name", "unknown")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name) or "unknown"

        HEALTH_DIR.mkdir(parents=True, exist_ok=True)
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {"_raw": body.decode(errors="replace")}

        out = {
            "received_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "automation_name": name,
            "automation_period": self.headers.get("automation-period"),
            "data": payload,
        }
        (HEALTH_DIR / f"{safe_name}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=2)
        )
        log(f"200 {safe_name} ({length} bytes) desde {self.client_address[0]}")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')

    def do_GET(self):
        # health check simple
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"health-receiver up")


if __name__ == "__main__":
    HESTIA_DIR.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    log(f"health-receiver arriba en puerto {PORT}")
    server.serve_forever()
