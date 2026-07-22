#!/usr/bin/env python3
"""Self-check de la reflexión de la noche. Corre: python3 test_evening.py
No toca red ni Telegram — solo la máquina de estados de mood/línea sobre un tmp."""
import json
import sys
import tempfile
import time
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import bot

tmp = Path(tempfile.mkdtemp())
bot.LIFE_SIGNALS = tmp / "life-signals"
bot.PENDING_EVENING = tmp / "pending-evening.json"
# el día que el cierre CIERRA (madrugada = ayer) — el código usa esto, no date.today()
dia = bot.logical_evening_date()


# regla de las 5am: madrugada cierra ayer; después de las 5, el día en curso
h = datetime.now().hour
esperado = (date.today() - timedelta(days=1)).isoformat() if h < 5 else date.today().isoformat()
assert bot.logical_evening_date() == esperado, (bot.logical_evening_date(), esperado)


def evening_json():
    f = bot.LIFE_SIGNALS / f"{dia}-evening.json"
    return json.loads(f.read_text()) if f.exists() else None


# sin cierre pendiente, cualquier texto pasa de largo
assert bot.take_evening_line("hola") is None

# tap de mood → guarda señal + marca pendiente
ack = bot.save_evening_mood("Good")
assert "Good" in ack
assert evening_json()["mood"] == "Good"
assert bot.PENDING_EVENING.exists()

# un slash-command NO se come como reflexión y deja la marca intacta
assert bot.take_evening_line("/hoy") is None
assert bot.PENDING_EVENING.exists()

# la línea suelta se captura, limpia la marca y queda en el JSON
r = bot.take_evening_line("cerré el informe, mañana arranco por el diseño")
assert "Daily" in r
assert evening_json()["linea"].startswith("cerré el informe")
assert not bot.PENDING_EVENING.exists()

# 'listo' cierra sin línea (día limpio: sin reflexión previa guardada)
(bot.LIFE_SIGNALS / f"{dia}-evening.json").unlink()
bot.save_evening_mood("Heavy")
r = bot.take_evening_line("listo")
assert "Cerrado" in r
assert "linea" not in evening_json()  # 'listo' no inventa línea
assert evening_json()["mood"] == "Heavy"

# marca del día lógico pero vieja (>30 min) ya no captura como corrección
bot.PENDING_EVENING.write_text(json.dumps(
    {"date": dia, "mood": "Good", "ts": time.time() - 3600}))
assert bot.take_evening_line("algo tarde") is None
assert not bot.PENDING_EVENING.exists()

# marca de otro día se ignora y se borra
otro = (datetime.strptime(dia, "%Y-%m-%d").date() - timedelta(days=1)).isoformat()
bot.PENDING_EVENING.write_text(json.dumps({"date": otro, "mood": "Sad", "ts": time.time()}))
assert bot.take_evening_line("algo") is None
assert not bot.PENDING_EVENING.exists()

print("OK — take_evening_line / save_evening_mood")
