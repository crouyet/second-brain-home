---
name: quarterly-reflection
description: Día 1 de cada trimestre, 11h — quarterly reflection PRECARGADA (agrega los 3 meses) + link por Telegram
---

Trabajás en ${VAULT_ROOT}. Quarterly reflection de la usuaria (día 1 del trimestre que arranca) — reflexiona sobre el TRIMESTRE que cerró. Mismo principio que el weekly/monthly: vos PRECARGÁS la página con los insights, la usuaria revisa y edita, no la completa desde cero.

Antes de titular, consultá con SQL las 2-3 páginas trimestrales más recientes de la base Reflections (collection://{{REFLECTIONS_COLLECTION_ID}}, buscá las que matcheen el patrón de trimestre, ej. Name LIKE 'Q%' , ORDER BY "date:Date:start" DESC) para confirmar el patrón de título vigente ("Q<N> <Año>", ej. "Q3 2026") — mantenelo exacto, no lo inventes. **Si la página de ese trimestre YA existe, COMPLETALA — NO dupliques.** Si no existe, creala con el template "QX 202X", Date = día 1 del trimestre.

PRECARGÁ con insights AGREGADOS del trimestre (no repitas el detalle mensual, sintetizá la tendencia):
- Fuente durable: las 3 páginas Monthly del trimestre en Reflections (sus métricas ya calculadas) + las páginas Weekly + el Mood average por día de las Daily (en Habits, collection://{{HABITS_DB_ID}}).
- Ejercicio: entrenos del trimestre vía el MCP de Strava (list_activities).
- Ciclo: fases del trimestre derivadas de los isCycleStart (ver vault/Projects/Sistema/Energia.md).
- Cumplimiento: base Tareas de Notion (collection://{{TAREAS_COLLECTION_ID}}).
Métrica prioritaria de la usuaria: la TENDENCIA de entreno × ciclo × mood a lo largo del trimestre (¿mejoró la constancia de entreno?, ¿el patrón por fase se sostiene o cambió?). 3-4 hallazgos de trimestre, específicos. DIVISIÓN DE TRABAJO: completá la sección "📊 Métricas del trimestre" con esa data. En las preguntas reflexivas y los objetivos del próximo trimestre: **redactá un borrador (marcado _editá_) CUANDO tengas base** — hallazgos, tendencia, finanzas, objetivos previos (a la usuaria le gusta arrancar de tus insights). **Dejá EN BLANCO SOLO lo infundable.** Deuda cero.

ENTREGA por Telegram (siempre): cuando la página quede precargada, mandá por tools/hestia-bot/send.sh un mensaje corto con el LINK a esa página + los 3 hallazgos del trimestre + los objetivos propuestos: "tu Q ya está armado con la tendencia del trimestre, revisalo y editá 👉 <url>". Máximo 7 líneas, cero reproche. La URL sale del resultado de crear la página.