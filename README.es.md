# 🏡 second-brain-home

[English](README.md) · **Español**

**Un sistema operativo de vida (agéntico) sobre Obsidian + Notion + Claude Code.**
Tu celular te despierta con el día ya decidido; la noche se cierra sola; tus reflexiones
(semanal → anual) llegan precargadas con métricas y vos solo agregás lo que una máquina no
puede saber. Lee tu energía desde tu ciclo menstrual y tu sueño, captura tu mood desde Apple
Health, y te habla por un bot de Telegram.

> La implementación de referencia está en español rioplatense (el tono cálido, cero
> reproche, es parte del diseño). Vos customizás todo.
>
> **Tu vault es solo una carpeta de archivos markdown** — Claude lo lee y escribe directo.
> Obsidian es *opcional* (una GUI linda para navegar/editar a mano); el sistema entero
> funciona sin él.

---

## Qué te da

| Pieza | Qué hace |
|---|---|
| **Tick de la mañana** | 8:30 — predice tu energía (ciclo + sueño), decide tus ≤3 tareas, te lo manda por Telegram. Cero preguntas. |
| **Tick de la noche** | 22:30 — cierra el día, un tap de mood, escribe tu fila del habit-tracker. |
| **Escalera de reflexiones** | Semanal → Mensual → Trimestral → Anual, cada una **precargada** con métricas (entreno×ciclo, mood, cumplimiento). Vos revisás; no llenás una hoja en blanco. |
| **Habit-tracker diario** | Una tabla de Notion, una fila por día. Claude auto-completa lo que tiene fuente (entrenos←Strava, mood/sueño/ciclo←Apple Health); vos llenás el resto. |
| **Bot de Telegram** | Tu canal de entrada/salida: `/hoy`, `/planificar`, `/ahora`, captura de texto libre. |
| **Health receiver** | Servidor local que ingiere Apple Health (mood, ciclo, sueño, medicación). |

---

## Connectors y apps que vas a necesitar

- **Notion** — 3 bases (Tareas, Reflections, Proyectos). Duplicás el template (ver `notion/TEMPLATE.md`).
- **Google Calendar** — un "Peak Calendar" dinámico (zonas de energía) + un calendario "Rutina".
- **Strava** — los entrenos alimentan el energy forecast y la métrica entreno×ciclo.
- **Apple Health** vía **[Health Auto Export](https://apps.apple.com/app/health-auto-export/id1115567069)** — una **app PAGA (~US$4/año)**. Alimenta mood, ciclo, sueño, medicación.
- **Telegram** — un bot que creás con @BotFather.
- **Claude Code** — el cerebro. Necesita `claude setup-token` (auth headless de larga duración).

Solo configurás las fuentes que realmente querés. Todo es opcional salvo Notion + Telegram.

---

## Arranque rápido

```bash
git clone git@github.com:crouyet/second-brain-home.git
cd second-brain-home
```

Después, en Claude Code, corré el setup guiado:

```
/setup
```

Te lleva paso a paso: elegir dónde vive tu vault, duplicar y conectar el template de Notion,
crear tu bot de Telegram, conectar Strava/Google Calendar, instalar el pipeline de Apple
Health, elegir **qué hábitos trackear y de dónde sale cada señal** (manual en Notion / Apple
Health / otro connector como Strava), y registrar las rutinas programadas.

¿Preferís hacerlo a mano? Ver [`setup/SETUP.md`](setup/SETUP.md).

---

## Cómo está construido

Sensores (Apple Health, Strava, Calendar) → Kernel (Claude + los docs de `Sistema/`:
heurística de energía, señales de riesgo, contrato de autonomía) → Actuadores (Telegram,
Notion). Recorrido completo en [`docs/architecture.md`](docs/architecture.md).

La portabilidad vive en un solo archivo: **`vault/Projects/Sistema/config.md`** — tus IDs de
Notion, timezone y mapeo señal→fuente. El `/setup` lo llena; vos lo editás. Los secretos nunca
tocan el repo — viven en `~/.hestia/*.env`.

---

## Privacidad

Este es un **repo público con cero datos personales**. El `vault/` trae solo
contenido de ejemplo ficticio. Tus datos reales (salud, finanzas, notas) quedan locales y
git-ignored. Nunca commitees `~/.hestia/`, extractos bancarios ni exports de `Raw/`.

## Licencia

MIT — ver [LICENSE](LICENSE).
