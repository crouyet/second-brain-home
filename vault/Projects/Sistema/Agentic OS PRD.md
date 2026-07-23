---
categories: [project-brief]
subjects: [sistema, agentic-os, prd]
status: active
version: v1.3
---

# Hestia 🏛️ — PRD del Agente OS

**Una línea**: Hestia (diosa del hogar, el agente master) le baja la carga mental a la usuaria **encargándose de cosas por ella** — entrega el día decidido, vigila las señales y registra todo lo que le cuenten; el input humano es siempre opcional.

**Anti-objetivo explícito**: esto NO es un sistema de tracking que le pide responder preguntas cada mañana y noche. Toda pieza que exija disciplina diaria de carga está mal diseñada — se elimina o se vuelve opcional.

## El problema

El sistema v1.0 funciona pero es **pull**: skills que hay que acordarse de invocar. la usuaria no las tocó — "no se presenta ante mis ojos". Dos fallas concretas:

1. **La mañana en cama.** Se despierta cansada, con frío, agarra el celu "por si alguien habló" y cae en el scroll. No es falta de intención: es fricción corporal + teléfono disponible.
2. **Parálisis de next.** Planear en vez de ejecutar. Lo que le funciona (probado en cocina): que alguien le diga la acción mínima — "prendé el horno, lavá las papas" — sin tener que pensarla ella.

## La usuaria

Perfil completo en [[../../Wiki/Perfil|Perfil]]. Lo que define el diseño: funcionamiento tipo TDAH (arranque entusiasta, ejecutivo diario trabado), push > pull, una acción > lista de opciones, cero culpa (semana caída = se retoma, deuda cero), ama los Atajos de Apple.

## Arquitectura: sensores → kernel → actuadores

| Capa | Qué hace | Piezas |
|---|---|---|
| **Sensores** — entra info sin esfuerzo | capturan estado real | **health-receiver** (sueño/ciclo/medicación, push automático en background, sin abrir nada) + **MCP health-auto-export** (bonus en vivo si la app está abierta), trampa IG/WhatsApp, check-in opcional por Telegram, **Peak Calendar**, Strava, mood de las Daily de Notion |
| **Kernel** — decide | reglas + señales + skills | [[Señales de riesgo]], reglas del [[README\|Sistema]] (máx 3, ×1.5, próxima acción física), prioridad predictiva vs. importancia real |
| **Actuadores** — se presenta solo | Hestia ante sus ojos | **Telegram** (mensaje de la mañana 8:30 + alertas + respuestas), [[Morning Gate]] (bloqueo físico), launcher "OS" ([[Atajos Apple]] §8), respuestas de UNA acción |

**Peak Calendar**: publica las zonas de energía del día en Google Calendar con IDs parseables (`rhythmZone.brainFog/morningPeak/dip/eveningPeak/windDown`). Claude las lee por el conector de calendar — integración gratis. Y la queja "a Peak le falta info" se resuelve al revés: las life-signals del pulso son la info que le falta; `/revision` compara predicho vs. reportado.

**Prioridad predictiva** (en qué orden el kernel mira señales): energía → plata → casa → comida/suplementos → estudio/trabajo.
**Importancia real de vida** (qué cuida más fuerte): plata → trabajo → comida/suplementos (impacta directo en mente y energía).

## Day in the life (v1.2 — Hestia)

1. **Despertar (8-9).** Downtime activo: IG/WhatsApp bloqueados hasta 09:30 ([[Morning Gate]]). la usuaria no tiene que hacer NADA.
2. **Sin nada que hacer la noche anterior**: los datos de cuerpo ya están en Apple Health porque la usuaria los carga como siempre — el MCP health-auto-export los expone en vivo, sin export ni Atajos ([[Atajos Apple]] §5).
3. **8:30 — el mensaje de la mañana por Telegram** ([[Mañana Hestia]]): el día ya decidido — energía predicha (ciclo + sueño + Peak, sin preguntarle), las ≤3 del día ordenadas, lo que toca hoy (guiso, chica, ropa), UNA señal si disparó. Al final, 3 botones opcionales 🪫🔋⚡️ — si los toca, Hestia recalibra; si no, no pasa nada, jamás insiste. Día de energía baja predicha → el mensaje arranca con la secuencia corporal y UNA sola tarea.
4. **Durante el día — Telegram es la boca de Hestia**: "compré sésamo 3200" → registrado · "tomé magnesio" → logueado · "qué hago" → UNA acción (`/ahora`, que sabe el bloque Peak y las [[../Casa/Rutinas|Rutinas]]) · "no doy más" → re-enganche mínimo sin culpa.
5. **Viernes 18h**: la lista del sábado llega armada. **Domingo 18h**: `/revision` — predicho vs. reportado, racha sin scroll, UNA mejora. **Día 5**: cierre de finanzas. Todo solo.

## Autonomía — el contrato formal (v1.3)

Las 3 reglas simples de v1 ahora son el [[Contrato de autonomía]] formal: 3 niveles
(actúa sola / 1 review de un agente del consejo / consejo completo) con triggers
concretos, más el techo permanente que no cambia con ningún nivel de confianza —
Hestia nunca paga, borra ni publica. Cada capacidad gradúa entre tiers vía el
[[Trust ledger]] (watch→queue→auto, 10 corridas ≥90% gradúa, <80% degrada).

## El consejo de subagentes (v1.3)

Cuatro voces con criterio estable, no disfraz: **la-contadora** (guardiana de plata,
veredicto ACERCA/ALEJA sobre `Finanzas/Plan.md`), **la-entrenadora** (lee cuerpo/ciclo/
energía, barato en haiku), **la-veterana** (verificadora fresh-eyes: solo spec+resultado,
nunca el proceso — PASS/FAIL de 1 línea), **la-abogada-del-diablo** (¿hace falta de
verdad, o es entusiasmo de arranque?). 2 desacuerdos entre ellas → decide la usuaria con
resumen de disenso de 3 líneas por lado.

## Leyes del OS (laws, not tips)

Toda regla lleva un número, un "nunca" o un check verificable. Las que ya existen en [[README|Sistema]] siguen. Nuevas del OS:

1. **Nunca retar.** Ni un reproche, jamás — ni en push, ni en respuesta, ni en revisión.
2. **Una acción por respuesta** cuando la usuaria está ejecutando. Las listas son para planificar, no para hacer.
3. **Cuerpo antes que mente** si energía=baja o frío: primero intervención corporal, después recién una tarea.
4. **El tick silencioso cuesta un centavo**: checks diarios en modelo barato/effort low; lo caro se despierta solo si hay algo actionable.
5. **Nada a Notion sin próxima acción física** (ya era ley; el tick de la mañana la aplica también).
6. **Toda señal se re-chequea**: un goal verificado una vez es una suposición con timestamp. Las [[Señales de riesgo]] son predicados que [[Mañana Hestia]] corre cada día.
7. **Hestia no interroga**: todo input humano es opcional; el sistema funciona igual si la usuaria no carga nada.

## Métricas de éxito

- **Streak de mañanas sin scroll antes de la liberación** (intentos de la trampa = contador visible en `/revision`).
- **% de días con ≤3 tareas y cumplidas** (vs. días sobrecargados).
- **Precisión de la energía predicha** (predicho vs. reportado en los botones opcionales, cuando haya datos).
- **% de deep work caído en bloques Peak ⚡️** (vs. desperdiciado en Dip).
- v0 exitosa si una mañana de baja energía: bloquea, no reta, saca de la cama con una acción corporal mínima, registra la señal, reduce el día a ≤3 acciones.

## Roadmap

| Versión | Qué entra | Se desbloquea cuando |
|---|---|---|
| **v1.1** | Morning Gate, `/ahora`, señales de riesgo, life-signals, Peak como sensor | base (incluido) |
| **v1.2 — Hestia** | Bot de Telegram (el canal), tick de la mañana 8:30 sin preguntas, **MCP health-auto-export** (fase del ciclo + sueño + medicación en vivo, sin reportar nada — con Health Auto Export Premium, app de terceros, en vez del Atajo casero), scheduled tasks, 3 reglas de autonomía | base (incluido) |
| **v1.3** | Consejo de subagentes (la-contadora, la-entrenadora, la-veterana, la-abogada-del-diablo) + [[Contrato de autonomía\|contrato de autonomía formal]] (3 niveles + techo permanente) + **[[Trust ledger]]** (watch→queue→auto: cada capacidad gradúa con 10 corridas ≥90%, demotion automática). Heurística de `energy_forecast` formalizada en [[Energia]], parámetros ajustables por `/revision`. Wellness App reencuadrada como laboratorio n=1 incubando en Hestia | base (incluido) |
| **v2 — el ser funcional genera plata** | (a) **Estudio** como pieza de primera clase, con bloques en Peak ⚡️ (study_work_stall_risk ya lo vigila). (b) **Loop de business models**: hipótesis → experimento mínimo → medir → matar o escalar. WIP=1 hipótesis activa. Extractito = candidato natural. Regla de gamificación: parte de lo generado financia upgrades del propio OS — más tiempo y plata pa gastarla en vos. | 4 semanas de streaks (mañanas sin scroll + ≤3 cumplidas) |
| **v2.1** | Dashboard de compu con datos vivos de Hestia — heredando la estética de tu home de Notion (la v0 conceptual): goals visibles, "Qué tal tu día Queen 💚", ciclo/energía/streaks reales | v1.3 andando |
| **v2.2** (baja prioridad — MCP health-auto-export ya resuelve lo importante) | App iOS nativa Hestia: HealthKit completo, background delivery, el check-in como widget | cuenta Apple Developer (US$99/año), solo si el MCP de terceros se queda corto |

## Decisiones abiertas (para `/revision`)

- **Calendarios legacy** "Rutina" y "Rutine Blocks" (bloques circadianos estáticos de un intento anterior): Peak los reemplaza siendo dinámico. Auditar si están muertos y archivarlos.
- Hora de liberación (default 09:30) — ajustar con datos reales de las primeras semanas.

## Qué NO es este OS

- No controla el iPhone: la barrera física es Screen Time nativo (la usuaria la configura una vez). unrot es capa opcional que maneja ella.
- No se construyó app propia con HealthKit — Health Auto Export (terceros, US$5,99/año) ya resuelve sueño/ciclo/entrenos/medicación en vivo; app propia queda en v2.2 solo si algún día no alcanza.
- No adopta la maquinaria de OS-para-código de la referencia (trust ledger, workers externos, worktrees) — sobre-ingeniería para un OS de vida. Fuente de los principios: [[../../Raw/2026-07-15 agentic-os-fable5-referencia|Raw]].

## Referencias

[[Morning Gate]] · [[Señales de riesgo]] · [[Atajos Apple]] · [[README|Sistema README]] · [[../Casa/Rutinas|Rutinas de Casa]] · `vault/Raw/life-signals/`
