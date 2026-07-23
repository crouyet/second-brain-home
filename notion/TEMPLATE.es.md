# Setup de Notion

*🌐 [English](TEMPLATE.md)*

El sistema lee y escribe cuatro bases de Notion. Camino más fácil: **duplicá el template
público** y después conectalo a Claude para que `/setup` descubra los IDs.

## 1. Duplicá el template

Abrí el template público y tocá **Duplicate / Duplicar** (arriba a la derecha) a tu workspace:
👉 https://www.notion.com/templates/second-brain-home

Después conectá el **connector de Notion** en Claude (ajustes de connectors de claude.ai). `/setup`
va a buscar en tu workspace las bases de abajo y a escribir sus IDs `collection://` en `config.md`.

## 2. Las bases (schema)

Si armás las tuyas en vez de duplicar, respetá estos:

### Tareas (`TAREAS_COLLECTION_ID`)
| Propiedad | Tipo | Notas |
|---|---|---|
| Task name | Title | |
| Due | Date | maneja la vista diaria + tu calendario |
| Status | Status | Backlog / TO-DO / In Progress / Done / Archived |
| Priority | Select | Low / Medium / High |
| Tags | Multi-select | tags de contexto: `🪫 Low Battery`, `⏲️ -5 mins`, `💻 Computer`, `🏙️ Away` |
| Project | Relation → Proyectos | opcional |
| Summary | Text | opcional |

### Reflections (`REFLECTIONS_COLLECTION_ID`)
Tiene las páginas Weekly / Monthly / Quarterly / Yearly. Un template de página por cadencia, cada
uno con una sección **📊 Métricas** (la llena Claude) arriba de las preguntas reflexivas (las llenás vos).
| Propiedad | Tipo | Notas |
|---|---|---|
| Name | Title | ej. "July Week 4", "June Monthly", "Q3 2026", "Yearly review Qs: 2026" |
| Date | Date | |
| Mood average | Multi-select | Amazing / Good / Neutral / Heavy / Angry / Sad |

### Habits — el habit-tracker diario (`HABITS_DB_ID`)
Una **tabla, una fila por día** (título `Day`, un `Date`). El template trae estas columnas;
renombrá/agregá/sacá para que encaje con tu vida. Claude auto-completa las columnas cuya fuente es
un connector; vos tildás las manuales.
| Columna | Tipo | Fuente |
|---|---|---|
| Mood (ojo con el espacio al final `Mood `) | Select (Amazing/Good/Neutral/Heavy/Angry/Sad) | apple-health *o* manual |
| Ciclo | Text | apple-health |
| Sueño (h) | Number | apple-health |
| Gym / Yoga / Bicis / Paseo | Checkbox | strava (ejercicio) |
| Suplements | Multi-select | apple-health / manual |
| Skin Care / Morning Routine | Select / Multi-select | manual |
| Lectura / Estudio · Socialize · Violin | Checkbox | manual |
| Working Hours · Power Nap | Number | manual |
| Workout · Progress | Formula | auto (rollup de lo de arriba) |

### Proyectos (`PROYECTOS_COLLECTION_ID`) — opcional
| Propiedad | Tipo |
|---|---|
| Name | Title |
| Status | Status |
| (relación a Tareas) | Relation |

## 3. Patrones de nombres (no los cambies a la ligera)

Las tasks de reflexión matchean las páginas por nombre, así que mantené el patrón:
`<Mes> Week <N>` · `<Mes> Monthly` · `Q<N> <Año>` · `Yearly review Qs: <Año>`.
