#!/usr/bin/env python3
"""health-receiver — recibe los POST de las automations REST API de
Health Auto Export y los guarda en vault/Raw/health/. Corre en la Mac,
no necesita que la app del iPhone esté abierta (Apple solo exige que
el iPhone se haya desbloqueado en algún momento).

Config en ~/.hestia/health-receiver.env:
    API_KEY=...
    PORT=9001
"""

import hmac
import ipaddress
import json
import os
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
    return Path(__file__).resolve().parents[2]


HEALTH_DIR = _vault_root() / "vault" / "Raw" / "health"


def log(msg: str) -> None:
    """Solo nombre de automation, tamaño y estado — nunca payload ni headers (PII/secretos)."""
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
MAX_BODY = 10 * 1024 * 1024  # los exports reales pesan < 1 MB
# ponytail: 0.0.0.0 es necesario para recibir del iPhone por LAN; el auth real
# es la API key + ALLOW_CIDR. TLS necesitaría un reverse proxy adelante.
BIND = ENV.get("BIND", "0.0.0.0")
ALLOW_CIDR = ENV.get("ALLOW_CIDR", "")  # ej. "192.168.1.0/24"; vacío = cualquier IP


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # usamos log() propio, no el default a stderr

    def _authorized(self) -> bool:
        """403 si la IP no entra en ALLOW_CIDR, 401 si la key no coincide."""
        peer = self.client_address[0]
        if ALLOW_CIDR and ipaddress.ip_address(peer) not in ipaddress.ip_network(ALLOW_CIDR):
            self.send_response(403)
            self.end_headers()
            log(f"403 IP fuera de ALLOW_CIDR: {peer}")
            return False
        if not hmac.compare_digest(self.headers.get("X-API-Key", ""), API_KEY):
            self.send_response(401)
            self.end_headers()
            log(f"401 rechazado desde {peer}")
            return False
        return True

    def do_POST(self):
        if not self._authorized():
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            self.send_response(400)
            self.end_headers()
            log("400 Content-Length inválido")
            return
        if length > MAX_BODY:
            self.send_response(413)
            self.end_headers()
            log(f"413 body de {length} bytes")
            return

        name = self.headers.get("automation-name", "unknown")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name) or "unknown"

        # Sin fallback a texto crudo: lo que no es JSON no entra al vault (los JSON
        # de acá los leen prompts autónomos; texto libre sería injection directa).
        try:
            payload = json.loads(self.rfile.read(length)) if length else {}
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            log(f"400 body no es JSON ({safe_name})")
            return

        HEALTH_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(HEALTH_DIR, 0o700)  # ciclo/meds/sueño: solo la usuaria

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
        # health check — autenticado, para no confirmarle a un escáner qué corre acá
        if not self._authorized():
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')


if __name__ == "__main__":
    HESTIA_DIR.mkdir(exist_ok=True)
    os.chmod(HESTIA_DIR, 0o700)  # acá vive la API key
    server = ThreadingHTTPServer((BIND, PORT), Handler)
    log(f"health-receiver arriba en puerto {PORT}")
    server.serve_forever()
