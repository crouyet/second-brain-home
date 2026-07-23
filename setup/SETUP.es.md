# Instalación manual

*🌐 [English](SETUP.md)*

Mejor usá el camino guiado — corré `/setup` en Claude Code y te lleva por todo esto.
Este archivo es el fallback / referencia manual. Todo lo que configurás termina en
`vault/Projects/Sistema/config.md` (IDs + preferencias) y `~/.hestia/*.env` (secretos).
**Los secretos nunca van en el repo.**

## 0. Prerequisitos
- macOS, `python3`.
- Claude Code con un token de larga duración: corré `claude setup-token`, guardalo en
  `~/.hestia/claude-token.env` como `CLAUDE_CODE_OAUTH_TOKEN=...` (`chmod 600`).
  Este es el punto único de falla del sistema — si el CLI se desloguea, se para todo.

## 1. El vault (Obsidian opcional)
El vault es solo una carpeta de markdown — ya viene en el clone como `vault/`. **No se copia:**
el repo clonado (ej. `~/second-brain-home`) es tu `VAULT_ROOT`; los tools lo resuelven por su
propia ubicación. Tus notas privadas viven en `vault/` pero quedan fuera de git (ver `.gitignore`).
```bash
cp vault/Projects/Sistema/config.example.md vault/Projects/Sistema/config.md
# opcional — solo si tu clone no está en la ubicación por defecto:
# mkdir -p ~/.hestia && echo "VAULT_ROOT=$(pwd)" > ~/.hestia/vault-root.env
```

## 2. Notion (obligatorio)
1. Duplicá el template → tu workspace (ver [`../notion/TEMPLATE.es.md`](../notion/TEMPLATE.es.md)).
2. Conectá el connector de Notion en Claude.
3. Encontrá el `collection://<uuid>` de tus bases **Tareas**, **Reflections**, **Habits**
   (el habit-tracker diario) y **Proyectos**; ponelos en `config.md` y en `~/.hestia/notion.env`:
   ```
   TAREAS_COLLECTION_ID=...
   REFLECTIONS_COLLECTION_ID=...
   HABITS_DB_ID=...
   PROYECTOS_COLLECTION_ID=...
   ```
4. Sugerido: conectá la base **Tareas** a [Notion Calendar](https://www.notion.so/product/calendar)
   (app gratis) para ver las tareas del día por su `Due` en un calendario real.

## 3. Telegram (obligatorio)
```bash
./tools/hestia-bot/configure.sh   # pide el token de @BotFather, extrae tu chat_id
```

## 4. Habit tracker — señal → fuente
En `config.md`, definí qué hábitos trackeás y de dónde sale cada señal
(`manual-notion` / `apple-health` / `strava` / `gcal`). Claude auto-completa las columnas con fuente.

## 5. Apple Health (solo si alguna fuente = apple-health)
Health Auto Export es una **app paga (~US$4/año)**: https://apps.apple.com/app/health-auto-export/id1115567069
```bash
./tools/health-receiver/install.sh   # auto-detecta la IP de tu Mac, escribe ~/.hestia/health-receiver.env
cp .mcp.json.template .mcp.json       # completá la IP + token del MCP de tu teléfono
```
En la app, agregá **4 automations REST** (Cycle, Mood, Sleep, Medications) → JSON, "Since Last
Sync", cada 6h, a `http://<ip-de-tu-mac>:9001/` con header `X-API-Key`. Ver
[`../tools/health-receiver/SETUP.md`](../tools/health-receiver/SETUP.md).

## 6. Strava / Google Calendar (opcionales)
Conectá los connectors en Claude. Para Calendar, creá un **Peak Calendar** (zonas de energía) y
un calendario **Rutina** (ver [`../docs/architecture.es.md`](../docs/architecture.es.md)).

## 7. Servicios + rutinas
```bash
./tools/hestia-bot/install.sh          # LaunchAgent del bot
./tools/health-receiver/install.sh     # LaunchAgent del receiver (si usás Apple Health)
```
Registrá las scheduled tasks de `scheduled-tasks/` (copialas a `~/.claude/scheduled-tasks/` o
crealas con el MCP scheduled-tasks), ajustando los horarios a tu timezone.

## 8. Smoke test
```bash
./tools/hestia-bot/send.sh "hola desde second-brain-home"   # debería llegar a tu Telegram
```
Después mandale `/hoy` a tu bot — debería leer `config.md` y armarte el día.
