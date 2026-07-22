---
name: revision-domingo
description: Viernes 17h — cierre de semana con intención: weekly reflection + revisión del sistema
---

Trabajás en ${VAULT_ROOT}. Cierre de semana de la usuaria (viernes a la tarde — el finde queda libre para procesar; la planificación de la semana es el lunes con el tick, NO acá).

PARTE 1 — Weekly reflection guiada (lo que la usuaria ama, con su template real):
Antes de titular, consultá con SQL las 2-3 páginas Weekly más recientes de la base Reflections (collection://{{REFLECTIONS_COLLECTION_ID}}, WHERE Name LIKE '%Week%' ORDER BY "date:Date:start" DESC) para confirmar el patrón vigente de nombres — es importante para la usuaria mantenerlo exacto, no inventarlo. Patrón vigente verificado 2026-07: "<Mes en inglés> Week <N>" (ej. "July Week 2", "June Week 1", "May Week 2") — pero priorizá lo que veas en esas 2-3 páginas reales por si cambió.
Numeración de semana N: es la Nth semana Lunes-Domingo que se solapa con ese mes, contando desde 1 en la semana que contiene el día 1 del mes (aunque esa semana arranque en el mes anterior). Ej.: si el 1 de agosto cae martes, la semana Lun-Dom que lo contiene es "Week 1" de agosto aunque haya empezado el lunes de julio; la semana siguiente es "Week 2".
Creá la página con ese título, template "Weekly reflection", Date = lunes de esta semana. Guiala por Telegram (tools/hestia-bot/send.sh) con las preguntas del template, de a una, cálidas y cortas: aprendizajes (de mí / relaciones / trabajo / finanzas), qué logré y agradezco + qué micro-acción repito, qué me drenó + a qué digo no, qué postergué, en qué avanzo 1% la próxima semana. Con sus respuestas (si responde — si no, llenala con lo observable y dejale las preguntas abiertas en la página, jamás insistir), completá la página.
Mood average de la semana: calculalo de vault/Raw/health/Mood.json (stateOfMind de los últimos 7 días, valenceClassification → mapear a las opciones Amazing/Good/Neutral/Heavy/Angry/Sad) y setealo en la propiedad "Mood average". Cruzalo con ciclo y sueño (vault/Raw/health/) y entrenos (Strava MCP): la lectura útil es contextual — ej. "entreno intenso en lútea con poco sueño te baja el mood al día siguiente" — no correlaciones sueltas.

PARTE 2 — Revisión del sistema (skill /revision, .claude/skills/revision/SKILL.md):
Cumplimiento y patrones de la base Tareas, barrido de tareas pateadas (máx 5 decisiones), Strava, racha de mañanas sin scroll (vault/Raw/life-signals/), señales disparadas.

Trust ledger y energía (vault/Projects/Sistema/Trust ledger.md + Energia.md):
- Comparar predicciones de energía vs. reportadas de la semana; si el patrón pide ajustar un umbral de Energia.md, proponelo y aplicalo.
- Actualizar la tabla Capacidades del ledger (corridas/aciertos de la semana); graduar queue→auto con 10 corridas ≥90%, degradar <80%.

UNA mejora al sistema: antes de aplicarla, verificala con el subagente la-veterana (Task tool, subagent_type "la-veterana", pasale SOLO spec + resultado). PASS → aplicar y changelog de vault/Projects/Sistema/README.md (nivel +0.1); FAIL → no aplicar, anotar por qué.

Señales validadas (Wellness App): si algo corrió sostenido esta semana en Hestia que confirma una señal de vault/Projects/Wellness App/README.md, anotalo en una línea en su sección Estado.

Cerrá por Telegram con los wins de la semana y recordá /chefcito + pedir viandas. Deuda cero, jamás reproche.