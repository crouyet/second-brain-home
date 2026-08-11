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

## Chefcito — kitchen module (optional)
`/setup` fills this in by **asking how YOU plan meals** — it does not assume the author's
structure, and it rewrites `Chefcito/Planes Semanales/_template.md` to match your answers.

- **enabled:** false
- **plans_weekly:** true   <!-- false = you decide day by day; the weekly planning mode stays off -->
- **meals_per_day:** 3     <!-- how many times you eat. Drives the demand table and the day columns -->
- **cooked_vs_stocked:** `lunch, dinner = cooked` · `breakfast = stocked`
  <!-- "cooked" comes out of a prep block; "stocked" just has to be there. Both get counted:
       "not planned" is not the same as "not counted" — an empty slot means no food -->
- **who_cooks:** `you, Sundays`
  <!-- one person or several, with days. If the day isn't fixed, say so — the plan uses a
       relative rule instead of inventing a day -->
- **nutrition_target:** ``
  <!-- optional, and only if a professional gave you one (e.g. "100g protein/day"). Empty =
       the plan still works, it just skips the quantity check. The system never invents one -->
- **always_in_the_kitchen:** `something healthy to snack on, cut vegetables`
  <!-- your floor of ready food. These become `origen: cocinado` products in productos.json:
       restocked by cooking, never by shopping -->
- **conditioning_signals:** ``
  <!-- optional: training, allergies, intolerances, cycle — only what you choose to share -->

> The **mechanics** don't change with your answers and shouldn't be edited out: declare the
> week's demand before picking recipes, declare how many portions each block yields, and
> check production ≥ demand. That's what keeps a plan from silently falling short.

## Relationships tracking (optional)
- **enabled:** false
- **VINCULOS_PROJECT_NAME:** `<Notion project name>`   <!-- if you keep a dedicated Notion project for nurturing relationships (e.g. "Relaciones"), name it here — /revision pulls its completed tasks into the weekly reflection. Leave empty to skip. -->
