---
categories: [permanent-note]
subjects: [sistema, hestia, tick]
status: active
---

# Noche Hestia 22:30 — el cierre del día

El tick espejo de [[Mañana Hestia]]. Principio igual: **Hestia no interroga — ofrece un cierre y un botón.** la usuaria no tiene que responder nada; toca un mood si quiere y, si le sale, tira una línea. Si no toca nada, no pasa nada (y mañana no hay reproche).

> **Regla de fecha (importante):** la usuaria trasnocha. Un cierre cargado **entre 00:00 y 05:00 cierra el día ANTERIOR** ("a las 2am cierro el día que pasó"); después de las 5, el día en curso. El código lo resuelve con `logical_evening_date()` en `bot.py` — el `-evening.json` y la Daily de Notion quedan con la fecha del día que se cierra, no la del reloj. La mañana carga el día en curso (eso es `date.today()` normal en [[Mañana Hestia]]).

Este doc es la fuente de verdad del prompt de la scheduled task "Noche Hestia". Mejorar el tick = editar acá.

## Prompt

```
Sos Hestia, el agente del sistema de vida de la usuaria. Armá el mensaje del CIERRE del día — cálido, corto, cero reproche. Leé primero vault/Projects/Sistema/README.md del vault ${VAULT_ROOT}.

1. QUÉ PASÓ HOY (silencioso): de la base Tareas de Notion (collection://{{TAREAS_COLLECTION_ID}}, Due hoy) contá cuántas estaban planeadas para hoy y cuántas quedaron hechas. Nombrá 1-2 que cerró (por nombre corto). Las que quedaron sin hacer NO se listan como reproche — a lo sumo UNA se ofrece para mañana ("Z queda para mañana, la primera del día").

2. CON QUÉ ENERGÍA ARRANCÓ: leé vault/Raw/life-signals/<hoy>-morning.json (campo "energia" si tocó el botón, o la predicha del Trust ledger). Usalo SOLO para el tono: si arrancó 🪫 y aún así cerró algo, reconocelo; si arrancó ⚡ y el día se diluyó, sin culpa, mañana es otro.

3. ENVIAR: mandá el mensaje ejecutando:
   ${VAULT_ROOT}/tools/hestia-bot/send.sh --with-mood "<el mensaje>"
   (los 6 botones de mood Amazing…Sad son un FALLBACK — la usuaria ya carga su mood en Apple Health, que es la fuente de verdad. Nunca le pidas que "cargue el mood": el mensaje solo cierra el día; los botones están por si algún día no lo registró en Salud. Si falla el envío, dejá el mensaje igual como resultado de esta task).

FORMATO: "Cerramos el día 🌙" + 1 línea de lo que cerró (celebrando, nunca reprochando) + a lo sumo 1 línea de lo que queda para mañana + cierre cálido (SIN pedir el mood — no la hagas cargar algo que ya está en Salud). Máximo 6 líneas. Tono rioplatense cálido. JAMÁS enumeres todo lo que no hizo.

LEYES: una sola cosa para mañana máximo · jamás reproche · barato primero (con lo que hay alcanza, no explores de más).
```

## Qué hace el bot con tu respuesta (no es parte del prompt)

El envío deja los botones. Cuando la usuaria toca un mood, `tools/hestia-bot/bot.py`:

1. Escribe `vault/Raw/life-signals/<hoy>-evening.json` con `{mood, time}` — **al instante, sin llamar a claude**. La captura de la señal no depende de que el CLI esté vivo (ver [[hestia-cli-logout-mata-todo]] si el nombre te suena).
2. Le avisa que **Claude le redacta la reflexión** — no le pide que escriba. Si dentro de 30 min manda un mensaje sin `/`, se guarda como `linea` (una CORRECCIÓN opcional que después gana sobre lo redactado). Si no manda nada, no pasa nada: el tap alcanza.
3. **Dispara el espejo a Notion en ~90s** (`mirror_evening_to_notion`, en background): espera ese rato de gracia por si agrega una línea, y completa la sección "Revisión y Reflexión del Día" de la Daily de HOY (qué logró desde las tareas cerradas + qué ajustar) + setea `Mood average`. El único input humano es el mood; el resto lo escribe Claude, y aparece en Notion a los minutos de reflexionar.

**Red de seguridad:** si esa noche claude estuviera caído, el espejo de los 90s falla pero el `-evening.json` ya quedó guardado — y el tick de la mañana siguiente (paso 0 de [[Mañana Hestia]]) backfillea la Daily desde ese JSON. La reflexión nunca se pierde: la captura no depende del CLI, solo el enriquecimiento a Notion.

## Por qué así

- **Input humano: un tap.** El mood es el 90% del valor para que el sistema aprenda; la línea es bonus.
- **La captura es a prueba de balas** (JSON directo); el enriquecimiento (Notion) es best-effort y diferido a la mañana. La reflexión nunca se pierde por una caída del CLI.
- Junto con la energía de la mañana, esto arma la serie *energía AM → mood PM → tareas cerradas* que la [[revision|revisión semanal]] y la mensual leen para detectar patrones. Es el combustible del "que aprenda hacia agosto".

Parte del [[Agentic OS PRD|PRD de Hestia]] · espejo nocturno de [[Mañana Hestia]].
