---
name: monthly-reflection
description: Día 1, 10h — monthly reflection: métricas automáticas + planificación del mes
---

Trabajás en ${VAULT_ROOT}. Monthly reflection de la usuaria (día 1 del mes) — reemplaza su flujo viejo de exportar CSV de hábitos a mano para pedirle correlaciones a GPT; ahora las hacés vos con los datos que fluyen solos.

Antes de titular, consultá con SQL las 2-3 páginas Monthly más recientes de la base Reflections (collection://{{REFLECTIONS_COLLECTION_ID}}, WHERE Name LIKE '%Monthly%' ORDER BY "date:Date:start" DESC) para confirmar el patrón vigente — es importante para la usuaria mantenerlo exacto, no inventarlo. Patrón vigente verificado 2026-07: "<Mes en inglés> Monthly" (ej. "May Monthly", "September Monthly") — pero priorizá lo que veas en esas 2-3 páginas reales por si cambió.

**Si la página de ese mes YA existe (mismo nombre, ej. "July Monthly"), COMPLETALA — NO dupliques.** Si no existe, creala con el título del patrón, template "Monthly reflection", Date = día 1.

SECCIÓN MÉTRICAS (automática, del mes que cerró):
- Mood: el `Mood average` de las páginas Daily del mes en Habits (collection://{{HABITS_DB_ID}}) — fuente DURABLE (la llena la reflexión diaria). NO uses vault/Raw/health/Mood.json como serie: es un snapshot que se sobreescribe en cada sync, no tiene historia; sirve solo como fallback del día más reciente.
- Ejercicio: entrenos del mes vía el MCP de Strava (list_activities) — fuente durable via API.
- Ciclo: fase de cada día derivada de los `isCycleStart` de vault/Raw/health/Cycle.json (ver [[Energia]]).
- Sueño: vault/Raw/health/Sleep.json (snapshot — si no hay historia del mes, seguí sin él).
- Cumplimiento: base Tareas de Notion (collection://{{TAREAS_COLLECTION_ID}}) — completadas vs. planificadas.
El análisis es CONTEXTUAL, no correlaciones sueltas. **Métrica prioritaria de la usuaria: entreno × ciclo** (ej. "entrenaste 8 veces, 6 en folicular; el mismo entreno sube tu mood en folicular y lo baja en lútea tardía"; "en menstrual entrenás poco y cerrás menos — el plan de esos días ya viene liviano"). Después el resto (sueño×mood, etc.). 3 hallazgos máximo, específicos y accionables. Si un dato no está, seguí sin él — deuda cero. Ojo: los primeros meses la serie es corta; decilo, no inventes correlaciones sin base.

DIVISIÓN DE TRABAJO: completá la sección "📊 Métricas del mes" del template con la data de arriba. En las preguntas reflexivas y de planificación: **redactá un borrador (marcado _editá_) CUANDO tengas base** — hallazgos, finanzas, objetivos, patrones (a la usuaria le gusta arrancar de tus insights). **Dejá EN BLANCO SOLO lo infundable** (introspección pura sin data). El objetivo del mes proponelo como borrador desde los hallazgos + los objetivos del mes anterior; ella decide.
También revisá los objetivos del mes anterior (página Monthly previa en Reflections si existe): qué acciones se movieron, en 2 líneas, sin reproche — eso es dato, va.

ENTREGA por Telegram (siempre, es lo que la usuaria espera): cuando la página Monthly ya quedó precargada (métricas + planificación borrador), mandá por tools/hestia-bot/send.sh un mensaje corto con **el link a esa página** + los 3 hallazgos + el objetivo propuesto: "tu Monthly ya está armada con las métricas y una propuesta de objetivo, revisala y editá 👉 <url>". Máximo 6 líneas, invitación a revisar, cero reproche. La URL sale del resultado de crear la página.

Las finanzas NO van acá — tienen su propio cierre el día 5 (cierre-finanzas-mensual).