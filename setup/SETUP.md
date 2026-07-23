# Manual setup

Prefer the guided path — run `/setup` in Claude Code and it walks you through all of this.
This file is the manual fallback / reference. Everything you configure lands in
`vault/Projects/Sistema/config.md` (IDs + preferences) and `~/.hestia/*.env` (secrets).
**Secrets never go in the repo.**

## 0. Prerequisites
- macOS, `python3`.
- Claude Code with a long-lived token: run `claude setup-token`, save it to
  `~/.hestia/claude-token.env` as `CLAUDE_CODE_OAUTH_TOKEN=...` (`chmod 600`).
  This is the system's single point of failure — if the CLI logs out, everything stops.

## 1. The vault (Obsidian optional)
The vault is just a folder of markdown — it already ships in the clone as `vault/`. **No copy:**
the cloned repo (e.g. `~/second-brain-home`) is your `VAULT_ROOT`; the tools resolve it from their
own location. Your private notes live in `vault/` but stay out of git (see `.gitignore`).
```bash
cp vault/Projects/Sistema/config.example.md vault/Projects/Sistema/config.md
# optional — only if your clone isn't the default location:
# mkdir -p ~/.hestia && echo "VAULT_ROOT=$(pwd)" > ~/.hestia/vault-root.env
```

## 2. Notion (required)
1. Duplicate the template → your workspace (see [`../notion/TEMPLATE.md`](../notion/TEMPLATE.md)).
2. Connect the Notion connector in Claude.
3. Find the `collection://<uuid>` of your **Tasks**, **Reflections**, **Daily habit-tracker**
   and **Projects** DBs; put them in `config.md` and in `~/.hestia/notion.env`:
   ```
   TAREAS_COLLECTION_ID=...
   REFLECTIONS_COLLECTION_ID=...
   HABITS_DB_ID=...
   PROYECTOS_COLLECTION_ID=...
   ```

## 3. Telegram (required)
```bash
./tools/hestia-bot/configure.sh   # asks for the @BotFather token, extracts your chat_id
```

## 4. Habit tracker — signal → source
In `config.md`, set which habits you track and where each signal comes from
(`manual-notion` / `apple-health` / `strava` / `gcal`). Claude auto-fills sourced columns.

## 5. Apple Health (only if any source = apple-health)
Health Auto Export is a **paid app (~US$4/yr)**: https://apps.apple.com/app/health-auto-export/id1115567069
```bash
./tools/health-receiver/install.sh   # auto-detects your Mac IP, writes ~/.hestia/health-receiver.env
cp .mcp.json.template .mcp.json       # fill in your phone's MCP IP + token
```
In the app, add **4 REST automations** (Cycle, Mood, Sleep, Medications) → JSON, "Since Last
Sync", every 6h, to `http://<your-mac-ip>:9001/` with header `X-API-Key`. See
[`../tools/health-receiver/SETUP.md`](../tools/health-receiver/SETUP.md).

## 6. Strava / Google Calendar (optional)
Connect the connectors in Claude. For Calendar, create a **Peak Calendar** (energy zones) and
a **Routine** calendar (see [`../docs/architecture.md`](../docs/architecture.md)).

## 7. Services + routines
```bash
./tools/hestia-bot/install.sh          # bot LaunchAgent
./tools/health-receiver/install.sh     # receiver LaunchAgent (if using Apple Health)
```
Register the scheduled tasks from `scheduled-tasks/` (copy to `~/.claude/scheduled-tasks/` or
create them via the scheduled-tasks MCP), adjusting times to your timezone.

## 8. Smoke test
```bash
./tools/hestia-bot/send.sh "hello from second-brain-home"   # should hit your Telegram
```
Then send `/hoy` to your bot — it should read `config.md` and build your day.
