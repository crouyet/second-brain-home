# Architecture

second-brain-home is an **agentic life OS**: sensors feed a kernel, the kernel decides,
actuators act. The kernel is Claude reading a handful of markdown docs; there is no ML and
no server you have to run in the cloud — just your Mac, your phone, and your accounts.

```
        SENSORS                       KERNEL                     ACTUATORS
  ┌──────────────────┐        ┌────────────────────┐       ┌──────────────────┐
  │ Apple Health     │        │ Claude Code        │       │ Telegram bot     │
  │  mood/cycle/     │──┐     │  + Projects/       │   ┌──▶│  morning/evening │
  │  sleep/meds      │  │     │    Sistema/*.md:   │   │   │  + free chat     │
  │ Strava workouts  │──┼────▶│   · Energia (fc)   │───┼──▶│ Notion           │
  │ Google Calendar  │  │     │   · Señales riesgo │   │   │  Tasks / Daily   │
  │ Notion Tasks     │──┘     │   · Contrato auto. │   └──▶│  Reflections     │
  └──────────────────┘        └────────────────────┘       └──────────────────┘
        life-signals  ◀───────────  config.md  ───────────▶  ~/.hestia/*.env
```

## The daily loop

- **Morning tick (≈08:30).** Reads last night's sleep + your cycle day and **predicts your
  energy** (`Energia.md` heuristic). Picks your ≤3 tasks from Notion, checks routines and
  risk signals, and sends a decided, no-questions message to Telegram. On low-energy days it
  leads with a body-care sequence and a single task.
- **Evening tick (≈22:30).** Closes the day: one mood tap (or auto from Apple Health), writes
  your **Daily habit-tracker** row. A late-night close (before ~5am) counts for the day that
  just ended — the "logical day" rule.

## The reflection ladder

Each cadence **aggregates the one below** and comes **pre-loaded with metrics** — you review,
you don't fill a blank page:

- **Daily** → a habit-tracker *table* (one row/day). Claude auto-fills columns that have a
  source (workouts←Strava, mood/sleep/cycle←Apple Health); you fill the rest.
- **Weekly → Monthly → Quarterly → Yearly** → reflection *pages*. Claude fills a **📊 Metrics**
  section (training×cycle, mood trend, completion) from durable data; you answer the
  reflective questions (only you know those). See each cadence's scheduled task.

The signature metric is **training × cycle**: how your workouts and mood move across your
menstrual phases, so you plan *with* your body instead of against it. It needs a few weeks of
data to become meaningful — that's the point of tracking now.

## Energy forecast

`Projects/Sistema/Energia.md` is a tunable, ML-free heuristic. Confidence order of sources:
`Raw/health/*.json` (from the receiver) → the Apple Health MCP → Calendar peak zones → default
"medium". Low-energy rules fire on `sleep < 6h` or menstrual phase (days 1–5). The weekly
reflection retunes the thresholds against the Trust ledger.

## Autonomy

`Contrato de autonomía.md` defines how much the system acts on its own: **L1** acts alone
(informational only, e.g. the morning tick), **L2** asks for one review before acting (e.g. a
shopping list, checked by the `la-contadora` agent), **L3** only advises. The `Trust ledger`
graduates a capability from *watch → queue → auto* as it proves itself.

## Portability

Nothing personal is hardcoded. Skills and tasks carry placeholders
(`{{TAREAS_COLLECTION_ID}}`, `${VAULT_ROOT}`) that Claude resolves from
`Projects/Sistema/config.md`. Secrets live in `~/.hestia/*.env`, never in the repo. Run
`/setup` to fill it all in.
