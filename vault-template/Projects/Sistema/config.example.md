---
categories: [permanent-note]
subjects: [sistema, config]
status: active
---

# config — the one place that makes this yours

`/setup` fills this in; you edit it afterward. **Every skill and scheduled task reads
its Notion IDs and preferences from here** instead of hardcoding them — so you never
touch prompt files. Copy this file to `config.md` (same folder) and complete it.

> **How skills use this:** prompts contain placeholders like `{{TAREAS_COLLECTION_ID}}`,
> `{{REFLECTIONS_COLLECTION_ID}}` and paths like `${VAULT_ROOT}`. When a skill runs, Claude
> resolves them from this file (the vault `CLAUDE.md` instructs it to). You never edit the
> prompts — you edit this config.

> IDs are not secrets (they're workspace identifiers), but real tokens/keys never go
> here — those live in `~/.hestia/*.env`, outside the repo.

## Assistant
- **name:** Hestia   <!-- the name your bot uses when it talks to you; rename freely -->
- **timezone:** America/Argentina/Buenos_Aires   <!-- your IANA tz -->
- **language:** es-AR   <!-- tone of the system prompts; adapt to taste -->

## Notion collections
Get these after duplicating & connecting the Notion template (`/setup` discovers them):
- **TAREAS_COLLECTION_ID:** `<uuid>`        <!-- Tasks DB -->
- **REFLECTIONS_COLLECTION_ID:** `<uuid>`   <!-- Reflections DB (Weekly→Yearly) -->
- **DAILY_HABIT_TABLE_ID:** `<uuid>`        <!-- Daily habit-tracker table -->
- **PROYECTOS_COLLECTION_ID:** `<uuid>`     <!-- Projects DB (optional) -->

## Habit tracker — signal → source
For each daily signal, where does it come from? One of:
`manual-notion` (you tick it) · `apple-health` · `strava` · `gcal`

| Signal | Source | Notes |
|---|---|---|
| mood | apple-health | State of Mind; or `manual-notion` to tap it yourself |
| cycle | apple-health | menstrual phase → drives energy forecast |
| sleep | apple-health | hours + timing |
| medications / supplements | apple-health | or `manual-notion` |
| workouts / training | strava | feeds the training×cycle metric |
| calendar events | gcal | Peak Calendar + Routine |

**habits_to_track:** (the checkbox columns in your Daily table — pick yours)
- gym, yoga, reading, water, skincare, ...

## Finance module (optional)
- **enabled:** false
- **statements_folder:** `vault/Projects/Finanzas/Resumenes/`
- **expected_files:** `MM-YYYY-visa.xls`, `MM-YYYY-master.xls`, `MM-YYYY-cuentas.pdf`
  <!-- the set that must be present for a month to be "closeable" — see Resumenes/README -->

## Shopping module (optional)
- **enabled:** false
- **details:** edit `vault/Projects/Compras/` with your shops, discount days, payment methods.
