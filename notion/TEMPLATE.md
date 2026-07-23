# Notion setup

*🌐 [Español](TEMPLATE.es.md)*

The system reads and writes four Notion databases. Easiest path: **duplicate the public
template**, then connect it to Claude so `/setup` can discover the IDs.

## 1. Duplicate the template

Open the public template and click **Duplicate** (top-right) into your workspace:
👉 https://www.notion.com/templates/second-brain-home

Then connect the **Notion connector** in Claude (claude.ai connector settings). `/setup`
will query your workspace for the databases below and write their `collection://` IDs into
`config.md`.

## 2. The databases (schema)

If you build your own instead of duplicating, match these:

### Tasks (`TAREAS_COLLECTION_ID`)
| Property | Type | Notes |
|---|---|---|
| Task name | Title | |
| Due | Date | drives the daily view + your calendar |
| Status | Status | Backlog / TO-DO / In Progress / Done / Archived |
| Priority | Select | Low / Medium / High |
| Tags | Multi-select | context tags: `🪫 Low Battery`, `⏲️ -5 mins`, `💻 Computer`, `🏙️ Away` |
| Project | Relation → Projects | optional |
| Summary | Text | optional |

### Reflections (`REFLECTIONS_COLLECTION_ID`)
Holds Weekly / Monthly / Quarterly / Yearly pages. One page template per cadence, each with
a **📊 Metrics** section (Claude fills) above the reflective questions (you fill).
| Property | Type | Notes |
|---|---|---|
| Name | Title | e.g. "July Week 4", "June Monthly", "Q3 2026", "Yearly review Qs: 2026" |
| Date | Date | |
| Mood average | Multi-select | Amazing / Good / Neutral / Heavy / Angry / Sad |

### Habits — the daily habit tracker (`HABITS_DB_ID`)
A **table, one row per day** (title `Day`, a `Date`). The template ships these columns;
rename/add/remove to fit your life. Claude auto-fills the columns whose source is a connector;
you tick the manual ones.
| Column | Type | Source |
|---|---|---|
| Mood (note the trailing space `Mood `) | Select (Amazing/Good/Neutral/Heavy/Angry/Sad) | apple-health *or* manual |
| Ciclo | Text | apple-health |
| Sueño (h) | Number | apple-health |
| Gym / Yoga / Bicis / Paseo | Checkbox | strava (exercise) |
| Suplements | Multi-select | apple-health / manual |
| Skin Care / Morning Routine | Select / Multi-select | manual |
| Lectura / Estudio · Socialize · Violin | Checkbox | manual |
| Working Hours · Power Nap | Number | manual |
| Workout · Progress | Formula | auto (rollup of the above) |

### Projects (`PROYECTOS_COLLECTION_ID`) — optional
| Property | Type |
|---|---|
| Name | Title |
| Status | Status |
| (relation to Tasks) | Relation |

## 3. Naming patterns (don't change these lightly)

The reflection tasks match pages by name, so keep the pattern:
`<Month> Week <N>` · `<Month> Monthly` · `Q<N> <Year>` · `Yearly review Qs: <Year>`.
