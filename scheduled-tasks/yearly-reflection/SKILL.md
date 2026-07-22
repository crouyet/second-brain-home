---
name: yearly-reflection
description: 1 de enero, 12h — yearly review PRECARGADA (agrega el año) + link por Telegram
---

Trabajás en ${VAULT_ROOT}. Yearly review de la usuaria (1 de enero) — reflexiona sobre el AÑO que cerró. Mismo principio que weekly/monthly/quarterly: vos PRECARGÁS la página con los insights del año, la usuaria revisa y edita, no la completa desde cero. Es la reflexión más estratégica del año — dale peso, pero sin inventar.

Antes de titular, consultá con SQL las páginas de review anual más recientes de la base Reflections (collection://{{REFLECTIONS_COLLECTION_ID}}, buscá el patrón de review anual, ORDER BY "date:Date:start" DESC) para confirmar el título vigente ("Yearly review Qs: <Año>", ej. "Yearly review Qs: 2026") — mantenelo exacto. **Si la página de ese año YA existe, COMPLETALA — NO dupliques.** Si no existe, creala con el template "Yearly review Qs: 202X", Date = 1 de enero del año.

PRECARGÁ con la síntesis del AÑO (agregá desde lo ya procesado, no recalcules el detalle diario):
- Fuente durable: las 4 páginas trimestrales (QX) del año + las Monthly, en Reflections — de ahí sale la narrativa del año.
- Ejercicio: resumen del año vía el MCP de Strava (list_activities): volumen, constancia, evolución.
- Ciclo × entreno × mood: la tendencia de todo el año (¿la constancia de entreno creció?, ¿aprendió a planificar con las fases?, ¿el mood promedio mejoró?).
- Cumplimiento y objetivos: cómo se movieron los objetivos trimestrales a lo largo del año (base Tareas collection://{{TAREAS_COLLECTION_ID}} + los objetivos de cada Q).
4-5 hallazgos de año, específicos, sin relleno motivacional vacío. DIVISIÓN DE TRABAJO: completá la sección "📊 Métricas del año" con esa data. En las preguntas reflexivas y los objetivos del año nuevo: **redactá un borrador (marcado _editá_) CUANDO tengas base** — evidencia del año, tendencia, finanzas, objetivos previos (a la usuaria le gusta arrancar de tus insights). **Dejá EN BLANCO SOLO lo infundable** (introspección pura sin data).

ENTREGA por Telegram (siempre): cuando la página quede precargada, mandá por tools/hestia-bot/send.sh un mensaje corto con el LINK a esa página + los 3-4 titulares del año + la invitación a revisarla con calma: "tu review del año ya está armada con la síntesis, tomate un rato y revisala 👉 <url>". Máximo 8 líneas, tono cálido de cierre de año, cero reproche. La URL sale del resultado de crear la página.