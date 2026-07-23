# Arquitectura

*🌐 [English](architecture.md)*

second-brain-home es un **sistema operativo de vida agéntico**: los sensores alimentan un kernel,
el kernel decide, los actuadores actúan. El kernel es Claude leyendo un puñado de docs markdown;
no hay ML ni un servidor que tengas que correr en la nube — solo tu Mac, tu teléfono y tus cuentas.

```
        SENSORES                      KERNEL                     ACTUADORES
  ┌──────────────────┐        ┌────────────────────┐       ┌──────────────────┐
  │ Apple Health     │        │ Claude Code        │       │ Bot de Telegram  │
  │  mood/ciclo/     │──┐     │  + Projects/       │   ┌──▶│  mañana/noche    │
  │  sueño/meds      │  │     │    Sistema/*.md:   │   │   │  + chat libre    │
  │ Strava entrenos  │──┼────▶│   · Energia (fc)   │───┼──▶│ Notion           │
  │ Google Calendar  │  │     │   · Señales riesgo │   │   │  Tareas / Daily  │
  │ Notion Tareas    │──┘     │   · Contrato auto. │   └──▶│  Reflections     │
  └──────────────────┘        └────────────────────┘       └──────────────────┘
        life-signals  ◀───────────  config.md  ───────────▶  ~/.hestia/*.env
```

## El loop diario

- **Tick de la mañana (≈08:30).** Lee el sueño de anoche + tu día de ciclo y **predice tu
  energía** (heurística de `Energia.md`). Elige tus ≤3 tareas de Notion, chequea rutinas y
  señales de riesgo, y manda un mensaje decidido y sin preguntas a Telegram. En días de poca
  energía arranca con una secuencia de cuidado del cuerpo y una sola tarea.
- **Tick de la noche (≈22:30).** Cierra el día: un tap de mood (o automático desde Apple Health),
  escribe tu fila del **habit-tracker diario**. Un cierre de madrugada (antes de las ~5am) cuenta
  para el día que recién terminó — la regla del "día lógico".

## La escalera de reflexiones

Cada cadencia **agrega la de abajo** y viene **precargada con métricas** — vos revisás, no
llenás una hoja en blanco:

- **Diario** → una *tabla* habit-tracker (una fila/día). Claude auto-completa las columnas que
  tienen fuente (entrenos←Strava, mood/sueño/ciclo←Apple Health); vos llenás el resto.
- **Semanal → Mensual → Trimestral → Anual** → *páginas* de reflexión. Claude completa una
  sección **📊 Métricas** (entreno×ciclo, tendencia de mood, cumplimiento) desde datos durables;
  vos respondés las preguntas reflexivas (esas solo las sabés vos). Ver la scheduled task de cada
  cadencia.

La métrica insignia es **entreno × ciclo**: cómo se mueven tus entrenos y tu mood a lo largo de
tus fases menstruales, para que planifiques *con* tu cuerpo en vez de contra él. Necesita unas
semanas de datos para volverse significativa — ese es el punto de trackear desde ahora.

## Predicción de energía

`Projects/Sistema/Energia.md` es una heurística ajustable, sin ML. Orden de confianza de fuentes:
`Raw/health/*.json` (del receiver) → el MCP de Apple Health → zonas peak del Calendar → default
"media". Las reglas de poca energía disparan con `sueño < 6h` o fase menstrual (días 1–5). La
reflexión semanal reajusta los umbrales contra el Trust ledger.

## Autonomía

`Contrato de autonomía.md` define cuánto actúa el sistema por su cuenta: **L1** actúa solo
(solo informativo, ej. el tick de la mañana), **L2** pide una revisión antes de actuar (ej. una
lista de compras, chequeada por el agente `la-contadora`), **L3** solo aconseja. El `Trust ledger`
gradúa una capacidad de *watch → queue → auto* a medida que se prueba a sí misma.

## Portabilidad

Nada personal está hardcodeado. Skills y tasks llevan placeholders
(`{{TAREAS_COLLECTION_ID}}`, `${VAULT_ROOT}`) que Claude resuelve desde
`Projects/Sistema/config.md`. Los secretos viven en `~/.hestia/*.env`, nunca en el repo. Corré
`/setup` para completarlo todo.
