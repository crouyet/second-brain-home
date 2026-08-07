# 🏡 second-brain-home

**English** · [Español](README.es.md)

**An agentic life-operating-system on top of Obsidian + Notion + Claude Code.**
Your phone wakes you with the day already decided; your evening closes itself; your
reflections (weekly → yearly) come pre-loaded with metrics so you only add what a
machine can't know. It reads your energy from your sleep and cycle, captures your mood
from Apple Health, and talks to you through a Telegram bot.

> Reference implementation is in Rioplatense Spanish (the warm, no-reproach tone is
> part of the design). Docs and setup are in English. You customize everything.
>
> **Your vault is just a folder of markdown files** — Claude reads and writes it directly.
> Obsidian is *optional* (a nice GUI to browse/edit by hand); the whole system runs without it.

---

## What you get

| Piece | What it does |
|---|---|
| **Morning tick** | 8:30 — predicts your energy (sleep + cycle), decides your ≤3 tasks, sends it to Telegram. Zero questions. |
| **Evening tick** | 22:30 — closes the day, one mood tap, writes your daily habit-tracker row. |
| **Reflection ladder** | Weekly → Monthly → Quarterly → Yearly, each **pre-loaded** with metrics (training×cycle, mood, completion). You review; you don't fill a blank page. |
| **Daily habit-tracker** | A Notion table, one row/day. Claude auto-fills what has a source (workouts←Strava, mood/sleep/cycle←Apple Health); you fill the rest. |
| **Telegram bot** | Your I/O channel: `/hoy`, `/planificar`, `/ahora`, free-text capture. |
| **Health receiver** | Local server that ingests Apple Health (mood, cycle, sleep, medications). |

---

## Connectors & apps you'll need

- **Notion** — 3 databases (Tasks, Reflections, Projects). Duplicate the template (see `notion/TEMPLATE.md`).
- **Google Calendar** — a dynamic "Peak Calendar" (energy zones) + a "Routine" calendar.
- **Strava** — workouts feed the energy forecast and the training×cycle metric.
- **Apple Health** via **[Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069)** — a **paid app (~US$4/year)**. Feeds mood, cycle, sleep, medications.
- **Telegram** — a bot you create with @BotFather.
- **Claude Code** — the brain. Requires `claude setup-token` (long-lived headless auth).

You only configure the sources you actually want. Everything is optional except Notion +
Telegram — cycle tracking is just one signal among several, not a requirement.

---

## Quickstart

```bash
git clone git@github.com:crouyet/second-brain-home.git
cd second-brain-home
```

Then, in Claude Code, run the guided setup:

```
/setup
```

It walks you through: choosing your vault location, duplicating & connecting the Notion
template, creating your Telegram bot, connecting Strava/Google Calendar, installing the
Apple Health pipeline, choosing **which habits to track and where each signal comes from**
(manual in Notion / Apple Health / another connector like Strava), and registering the
scheduled routines.

Prefer to do it by hand? See [`setup/SETUP.md`](setup/SETUP.md).

---

## How it's built

Sensors (Apple Health, Strava, Calendar) → Kernel (Claude + the `Sistema/` docs: energy
heuristic, risk signals, autonomy contract) → Actuators (Telegram, Notion). Full
walkthrough in [`docs/architecture.md`](docs/architecture.md).

Portability lives in one file: **`vault/Projects/Sistema/config.md`** — your Notion IDs,
timezone, and signal→source mapping. `/setup` fills it; you edit it. Secrets never touch
the repo — they live in `~/.hestia/*.env`.

Before you install: [`docs/security.md`](docs/security.md) lists what this system exposes,
how likely each risk actually is, and which parts are optional.

---

## Privacy

This is a **public repo with zero personal data**. The `vault/` ships only
fictional seed content. Your real data (health, finances, notes) stays local and is
git-ignored. Never commit `~/.hestia/`, bank statements, or `Raw/` exports.

## License

MIT — see [LICENSE](LICENSE).
