#!/usr/bin/env python3
"""hestia-bot — el canal de Telegram de Hestia.

Long-polling contra la API de Telegram (stdlib pura, sin dependencias).
Rutea mensajes de la usuaria a `claude -p` (skills del vault) y procesa los
botones opcionales del mensaje de la mañana.

Config en ~/.hestia/telegram.env:
    TELEGRAM_TOKEN=123456:ABC...
    CHAT_ID=123456789
"""

import json
import os
import re
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

HESTIA_DIR = Path.home() / ".hestia"
ENV_FILE = HESTIA_DIR / "telegram.env"
TOKEN_FILE = HESTIA_DIR / "claude-token.env"  # CLAUDE_CODE_OAUTH_TOKEN=... (chmod 600)
PENDING_EVENING = HESTIA_DIR / "pending-evening.json"  # cierre del día esperando la línea
LOG_FILE = HESTIA_DIR / "bot.log"

CLAUDE_TIMEOUT = 600  # las skills pueden tardar (Notion, análisis)


def _read_env_file(path: Path) -> dict:
    """Lee un archivo simple KEY=VALUE (ignora comentarios y vacíos). {} si no existe."""
    out = {}
    if path.exists():
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip()
    return out


# Portabilidad: el /setup escribe estos archivos en ~/.hestia/. Defaults sensatos.
VAULT_REPO = Path(
    _read_env_file(HESTIA_DIR / "vault-root.env").get(
        "VAULT_ROOT", str(Path.home() / "obsidian-second-brain")
    )
).expanduser()
LIFE_SIGNALS = VAULT_REPO / "vault" / "Raw" / "life-signals"

# IDs de colecciones Notion (el /setup los descubre y escribe en ~/.hestia/notion.env)
_notion = _read_env_file(HESTIA_DIR / "notion.env")
TAREAS_COLLECTION = _notion.get("TAREAS_COLLECTION_ID", "")
REFLECTIONS_COLLECTION = _notion.get("REFLECTIONS_COLLECTION_ID", "")


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with LOG_FILE.open("a") as f:
        f.write(line + "\n")


def load_env() -> dict:
    if not ENV_FILE.exists():
        sys.exit(f"Falta {ENV_FILE} — ver tools/hestia-bot/SETUP.md")
    env = {}
    for raw in ENV_FILE.read_text().splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    for key in ("TELEGRAM_TOKEN", "CHAT_ID"):
        if not env.get(key):
            sys.exit(f"Falta {key} en {ENV_FILE}")
    return env


def api(token: str, method: str, params: dict) -> dict:
    data = urllib.parse.urlencode(
        {k: v if isinstance(v, str) else json.dumps(v) for k, v in params.items()}
    ).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data)
    with urllib.request.urlopen(req, timeout=70) as resp:
        return json.load(resp)


def send(token: str, chat_id: str, text: str) -> None:
    # Telegram corta en 4096; los resúmenes de skills pueden pasarse
    for i in range(0, len(text), 4000):
        api(token, "sendMessage", {"chat_id": chat_id, "text": text[i : i + 4000]})


def claude_env() -> dict:
    """Env para el subprocess de claude. Inyecta el token long-lived si existe:
    launchd no siempre llega al Keychain, así que el token por env lo hace
    determinista (ver TOKEN_FILE)."""
    env = os.environ.copy()
    if TOKEN_FILE.exists():
        for raw in TOKEN_FILE.read_text().splitlines():
            line = raw.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def run_claude(prompt: str) -> str:
    """Corre claude headless en el repo del vault (skills + CLAUDE.md disponibles)."""
    try:
        out = subprocess.run(
            [
                "claude", "-p", prompt,
                "--permission-mode", "acceptEdits",
                "--model", "sonnet",
            ],
            cwd=VAULT_REPO,
            capture_output=True,
            text=True,
            timeout=CLAUDE_TIMEOUT,
            env=claude_env(),
        )
        if out.returncode != 0:
            log(f"claude error: {out.stderr[:500]}")
            return "Se me trabó procesando eso — probá de nuevo en un rato."
        return out.stdout.strip() or "Hecho."
    except subprocess.TimeoutExpired:
        return "Se cortó por tiempo — mandámelo de nuevo en un rato."
    except FileNotFoundError:
        return "No encuentro el CLI de claude en esta Mac."


def save_checkin(energia: str) -> str:
    """Botón opcional del mensaje de la mañana → señal del día."""
    LIFE_SIGNALS.mkdir(parents=True, exist_ok=True)
    f = LIFE_SIGNALS / f"{date.today().isoformat()}-morning.json"
    data = json.loads(f.read_text()) if f.exists() else {"date": date.today().isoformat()}
    data["energia"] = energia
    data["time"] = datetime.now().strftime("%H:%M")
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    respuestas = {
        "baja": "Anotado. Día liviano entonces: primero cuerpo, después UNA cosa chica. 🧉",
        "media": "Anotado. Vamos con calma con lo del día. 💪",
        "alta": "Anotado. Día para aprovechar el Peak ⚡️",
    }
    return respuestas.get(energia, "Anotado.")


def logical_evening_date() -> str:
    """El día que un cierre CIERRA. la usuaria trasnocha: un cierre cargado entre 00:00 y 05:00
    es del día anterior (a las 2am 'cierro el día que pasó'). Después de las 5, el día en curso."""
    d = datetime.now()
    if d.hour < 5:
        return (d.date() - timedelta(days=1)).isoformat()
    return d.date().isoformat()


def save_evening_mood(mood: str) -> str:
    """Botón del cierre del día → señal de la noche + marca para capturar la línea.
    Escribe la señal ya (sin claude): la captura no depende de que el CLI esté vivo."""
    LIFE_SIGNALS.mkdir(parents=True, exist_ok=True)
    dia = logical_evening_date()
    f = LIFE_SIGNALS / f"{dia}-evening.json"
    data = json.loads(f.read_text()) if f.exists() else {"date": dia}
    data["mood"] = mood
    data["time"] = datetime.now().strftime("%H:%M")
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    PENDING_EVENING.write_text(json.dumps(
        {"date": dia, "mood": mood, "ts": time.time()}))
    return (f"Anotado {mood} 🌙. Te lo dejo redactado en la Daily en un toque; "
            "si querés corregir o agregar algo, mandámelo ahora. Sino, descansá.")


HOY_PROMPT = (
    "Armá el vistazo del día de la usuaria para Telegram, máximo 10 líneas. "
    "Leé: tareas Due hoy de la base Tareas de Notion "
    f"(collection://{TAREAS_COLLECTION}), rutinas vencidas de "
    "vault/Projects/Casa/Rutinas.md, y los calendarios (Peak Calendar dinámico, "
    "calendario Rutina —está incompleto, tomalo como intención—, eventos del día) "
    "SOLO como contexto para ordenar y detectar choques — no listes eventos; "
    "mencioná uno únicamente si condiciona el día. Tono rioplatense cálido, "
    "decidido, cero preguntas, jamás reproche."
)

FINANZAS_PROMPT = (
    "Leé vault/Projects/Finanzas/Plan.md y respondé en máximo 5 líneas: los 3 "
    "números del tracker del mes, el estado del plan de deuda/precancelación que "
    "figure en Plan.md, y UNA acción si hay algo pendiente. Tono cálido, sin sermón."
)

# ponytail: ruteo por regex, un router con NLU cuando las reglas se queden cortas
# Suplementos/medicación: NO se loguean acá — vienen automático por el MCP
# health-auto-export (ver .mcp.json), que lee directo de Apple Health.
ROUTES = [
    (re.compile(r"^\s*(compr[eé]|registr[aá] compra)\b", re.I),
     lambda t: run_claude(f"/compras registrar: {t}")),
    (re.compile(r"^\s*/compras\b", re.I), lambda t: run_claude("/compras")),
    (re.compile(r"^\s*(qu[eé] hago|/ahora|ahora)\b", re.I), lambda t: run_claude("/ahora")),
    (re.compile(r"^\s*/hoy\b", re.I), lambda t: run_claude(HOY_PROMPT)),
    (re.compile(r"^\s*(/planificar\b|tarea:|agend[aá]\b|tengo que\b)", re.I),
     lambda t: run_claude(f"/planificar {t}")),
    (re.compile(r"^\s*/chefcito\b", re.I), lambda t: run_claude(f"/chefcito {t}")),
    (re.compile(r"^\s*/revision\b", re.I), lambda t: run_claude("/revision")),
    (re.compile(r"^\s*/finanzas\b", re.I), lambda t: run_claude(FINANZAS_PROMPT)),
    (re.compile(r"^\s*cerr[aá]\b.*\b(mes|finanzas|lo que hay)", re.I),
     lambda t: run_claude(f"/cierre-finanzas — pedido de la usuaria por Telegram: {t}")),
    (re.compile(r"\bcocinar\b", re.I), lambda t: run_claude("/ahora cocinar")),
    (re.compile(r"me ca[ií]|no doy m[aá]s", re.I),
     lambda t: run_claude(f"me caí del sistema — dijo: {t}")),
]

# El menú que aparece al tocar "/" en Telegram (se registra en cada arranque)
COMMANDS = [
    {"command": "ahora", "description": "qué hago — UNA acción de ≤5 min"},
    {"command": "hoy", "description": "vistazo del día: tareas + rutinas"},
    {"command": "planificar", "description": "cargar tareas (brain-dump → Notion)"},
    {"command": "compras", "description": "lista de compras / registrar"},
    {"command": "chefcito", "description": "meal prep según inventario y energía"},
    {"command": "revision", "description": "revisión semanal"},
    {"command": "finanzas", "description": "cómo vengo: los 3 números del mes"},
]

FALLBACK_PROMPT = (
    "Sos Hestia, el agente del sistema de vida de la usuaria (leé vault/CLAUDE.md y "
    "vault/Projects/Sistema/README.md). Te llegó este mensaje suyo por Telegram. "
    "Si es un dato para registrar, registralo donde corresponda en el vault. "
    "Si es una pregunta, respondé corto y práctico, rioplatense, sin sermones. "
    "Respuesta máxima: 6 líneas. Mensaje: "
)


def take_evening_line(text: str):
    """Si hay un cierre de HOY esperando y el texto es una línea suelta (no un comando),
    la guarda en la señal de la noche. El espejo a Notion lo hace el tick de la mañana
    desde este JSON — así la captura NO depende de que el CLI de claude esté vivo.
    Devuelve la respuesta, o None si el texto no es la reflexión."""
    if not PENDING_EVENING.exists():
        return None
    try:
        pend = json.loads(PENDING_EVENING.read_text())
    except Exception:
        PENDING_EVENING.unlink(missing_ok=True)
        return None
    dia = pend.get("date", "")
    if dia != logical_evening_date():
        PENDING_EVENING.unlink(missing_ok=True)  # marca vieja, ignorar
        return None
    if time.time() - pend.get("ts", 0) > 1800:  # 30 min: pasado ese rato ya no es la corrección
        PENDING_EVENING.unlink(missing_ok=True)
        return None
    # ponytail: la línea es una CORRECCIÓN opcional (claude redacta la reflexión igual). Dentro
    # de la ventana, tu próximo mensaje SIN "/" la sobrescribe. Solo los slash-commands escapan.
    if text.strip().startswith("/"):
        return None  # es un comando explícito, no la corrección
    PENDING_EVENING.unlink(missing_ok=True)
    linea = "" if text.strip().lower() in ("listo", "nada", "ok", "-") else text.strip()
    f = LIFE_SIGNALS / f"{dia}-evening.json"
    data = json.loads(f.read_text()) if f.exists() else {"date": dia}
    if linea:
        data["linea"] = linea
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return "Anotado, lo sumo a tu Daily 🌙" if linea else "Cerrado. Descansá 🌙"


def mirror_evening_to_notion() -> None:
    """Espeja la reflexión de HOY a la Daily de Notion (Mood + redacción), en background y
    tras un rato de gracia por si la usuaria agrega una línea. Best-effort: si claude está caído no
    pasa nada, el tick de la mañana la backfillea desde el mismo JSON. Idempotente: completar
    la misma sección dos veces no duplica."""
    time.sleep(90)  # ponytail: gracia fija para una línea; si escribe más tarde, la toma la mañana
    f = LIFE_SIGNALS / f"{logical_evening_date()}-evening.json"
    if not f.exists():
        return
    data = json.loads(f.read_text())
    dia = data["date"]  # día lógico que cierra (puede ser ayer si cargó de madrugada)
    weekday_en = datetime.strptime(dia, "%Y-%m-%d").strftime("%A")
    ajuste = (f"poné tal cual: {data['linea']}. " if data.get("linea")
              else "redactá UNA sugerencia corta desde lo que quedó sin cerrar ese día y el mood, cero reproche. ")
    prompt = (
        f"Completá SOLO la sección 'Revisión y Reflexión del Día' de la Daily del {dia} en la base "
        f"Reflections de Notion (collection://{REFLECTIONS_COLLECTION}: página con "
        f"Date = {dia} y Name '{weekday_en} Daily'; si no existe, creala con el template 'Daily "
        f"Reflection', Name '{weekday_en} Daily', Date = {dia}). "
        f"MOOD: si vault/Raw/health/Mood.json tiene un stateOfMind cuyo start cae en {dia}, usá ESE "
        "como mood real — mapeá su valenceClassification+labels a la opción más cercana de la property "
        "Mood average (Amazing/Good/Neutral/Heavy/Angry/Sad) y mencioná los labels (ej. calm, drained) "
        f"en la reflexión. Si no hay, usá Mood average = {data.get('mood', '')} (el tap). "
        f"En '¿Qué logré hoy?' resumí en 1-2 bullets las tareas que la usuaria cerró el {dia} (base Tareas, "
        f"Due {dia}, hechas). En '¿Qué necesito ajustar para mañana?': {ajuste}"
        "No toques el resto de la página ni respondas texto largo."
    )
    run_claude(prompt)


def handle_text(text: str) -> str:
    evening = take_evening_line(text)
    if evening is not None:
        return evening
    for pattern, handler in ROUTES:
        if pattern.search(text):
            return handler(text)
    return run_claude(FALLBACK_PROMPT + text)


def responder(token: str, chat_id: str, text: str) -> None:
    """Corre en su propio thread: acusa recibo ya, responde cuando está."""
    try:
        send(token, chat_id, "⏳ dale, dame un toque")
        reply = handle_text(text)
        send(token, chat_id, reply)
        log(f">> {reply[:80]}")
    except Exception as e:
        log(f"handler error: {e}")
        try:
            send(token, chat_id, "Uy, algo se rompió procesando eso. Quedó logueado.")
        except Exception:
            pass


def main() -> None:
    env = load_env()
    token, chat_id = env["TELEGRAM_TOKEN"], env["CHAT_ID"]
    log("hestia-bot arriba")
    try:
        api(token, "setMyCommands", {"commands": COMMANDS})
    except Exception as e:  # sin menú no es fatal, el bot sigue
        log(f"setMyCommands error: {e}")
    offset = 0
    poll_errors = 0
    while True:
        try:
            updates = api(token, "getUpdates", {"offset": offset, "timeout": 50})
            poll_errors = 0
        except Exception as e:  # red caída, Mac despertando, etc.
            poll_errors += 1
            log(f"poll error ({poll_errors}/10): {e}")
            if poll_errors >= 10:
                # ponytail: no reconectar a mano — morir limpio, launchd (KeepAlive) relanza
                log("10 poll errors seguidos — reinicio via launchd")
                sys.exit(1)
            time.sleep(10)
            continue
        for u in updates.get("result", []):
            offset = u["update_id"] + 1
            try:
                if "callback_query" in u:
                    cq = u["callback_query"]
                    if str(cq["message"]["chat"]["id"]) != chat_id:
                        continue
                    data = cq.get("data", "")
                    if data.startswith("mood:"):
                        reply = save_evening_mood(data.split(":", 1)[1])
                        threading.Thread(target=mirror_evening_to_notion, daemon=True).start()
                    else:
                        reply = save_checkin(data)
                    api(token, "answerCallbackQuery", {"callback_query_id": cq["id"]})
                    send(token, chat_id, reply)
                elif "message" in u and "text" in u["message"]:
                    msg = u["message"]
                    if str(msg["chat"]["id"]) != chat_id:
                        log(f"chat_id desconocido ignorado: {msg['chat']['id']}")
                        continue
                    text = msg["text"]
                    log(f"<< {text[:80]}")
                    # ponytail: thread por mensaje — el poll nunca queda sordo mientras
                    # una skill corre; si algún día se apilan corridas de claude, poner
                    # un semáforo de a 2
                    threading.Thread(
                        target=responder, args=(token, chat_id, text), daemon=True
                    ).start()
            except Exception as e:
                log(f"handler error: {e}")


if __name__ == "__main__":
    HESTIA_DIR.mkdir(exist_ok=True)
    main()
