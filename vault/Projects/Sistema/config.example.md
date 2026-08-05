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
- **HABITS_DB_ID:** `<uuid>`                <!-- "Habits" DB = the daily habit tracker -->
- **REFLECTIONS_COLLECTION_ID:** `<uuid>`   <!-- "Reflections" DB (Weekly→Yearly, Mood average) -->
- **TAREAS_COLLECTION_ID:** `<uuid>`        <!-- Tasks DB -->
- **PROYECTOS_COLLECTION_ID:** `<uuid>`     <!-- Projects DB (optional) -->

## Habit tracker — signal → source
The template's **Habits** DB (daily, one row/day) has columns like Mood, Gym, Yoga, Bicis,
Paseo, Lectura/Estudio, Morning Routine, Skin Care, Suplements, Working Hours, Power Nap,
Socialize, Violin, Commet, Ciclo, Sueño (h). Rename/add/remove to fit your life (the template
explains how). For each signal, where does it come from? One of:
`manual-notion` (you tick it) · `apple-health` · `strava` · `gcal`

| Signal | Source | Habits column |
|---|---|---|
| mood | apple-health | `Mood ` (or manual) |
| cycle *(only if this applies to you — drop the row otherwise)* | apple-health | `Ciclo` → drives energy forecast |
| sleep | apple-health | `Sueño (h)` |
| supplements | apple-health / manual | `Suplements` |
| workouts | strava | `Gym` / `Yoga` / `Bicis` |
| everything else | manual-notion | Skin Care, Reading, Working Hours, … |

## Finance module (optional)
- **enabled:** false
- **statements_folder:** `vault/Projects/Finanzas/Resumenes/`
- **expected_files:** `MM-YYYY-visa.xls`, `MM-YYYY-master.xls`, `MM-YYYY-cuentas.pdf`
  <!-- the set that must be present for a month to be "closeable" — see Resumenes/README -->

## Shopping module (optional)
- **enabled:** false
- **details:** edit `vault/Projects/Compras/` with your shops, discount days, payment methods.

## Relationships tracking (optional)
- **enabled:** false
- **VINCULOS_PROJECT_NAME:** `<Notion project name>`   <!-- if you keep a dedicated Notion project for nurturing relationships (e.g. "Relaciones"), name it here — /revision pulls its completed tasks into the weekly reflection. Leave empty to skip. -->
