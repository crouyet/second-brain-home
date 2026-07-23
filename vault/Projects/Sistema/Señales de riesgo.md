---
categories: [permanent-note]
subjects: [sistema, señales, riesgo]
status: active
---

# Señales de riesgo — los predicados del kernel

Regla madre: **un goal verificado una vez es una suposición con timestamp.** Estas señales no son diagnósticos de una vez — el pulso de 7:30 las re-chequea cada día con lo que tenga a mano (life-signals, Notion, Peak, vault). Consumidores: pulso diario, `/ahora`, `/revision`.

## Formato de respuesta (obligatorio)

Cuando una señal dispara, nada de consejos largos:

> "Veo riesgo de **[X]** por [2 señales]. No lo resolvemos pensando. Hacé esto ahora: **[acción de 5 min]**. Después recién [siguiente paso]."

Si intenta abrir IG/WhatsApp antes de hora:

> "Esto es el loop. Primero cuerpo: abrigo + agua + pulso mínimo. Después decidimos."

## Las 6 señales

### `morning_scroll_risk`
Dispara con 2+ de: intento de abrir IG/WhatsApp antes del pulso · sueño corto · energía baja reportada · frío/cansancio reportado · cero comida/suplementos.
**Acción**: secuencia corporal de [[Morning Gate]], una por vez.

### `energy_crash_risk`
Dispara con: mal sueño + ciclo cercano + (entreno intenso ayer O cero movimiento) + suplementos omitidos.
**Acción**: hoy solo tareas `🪫 Low Batery`; suplemento + comida base ahora; no agendar nada nuevo.

### `money_avoidance_risk`
Dispara con 2+ de: tareas financieras vencidas en Notion · cierre mensual no hecho pasado el día 5 · gastos/compras sin registrar · delivery subiendo o comida base fallando.
**Acción**: UNA micro-acción financiera de 5 min (abrir el resumen, registrar la compra de ayer). El cierre completo va como tarea con Due, no como culpa. Contexto: [[../Finanzas/Plan|Plan de Finanzas]].

### `house_decay_risk`
Dispara con 2+ de: micro-tareas de casa no hechas 3 días ([[../Casa/Rutinas|Rutinas]] vencidas) · platos/ropa acumulados reportados · baja energía + casa visualmente cargada.
**Acción**: UN pomodoro con micro-tarea de casa en el descanso — nunca "ordenar todo".

### `food_mind_risk`
Dispara con 2+ de: sin viandas para la semana · sin desayuno/snacks base · suplementos omitidos 2+ días · compras no registradas · fase del ciclo que pide más soporte.
**Acción**: pedir viandas ahora (5 min) o `/chefcito` nivel energía baja. Comida y suplementos impactan directo en mente y energía — por eso está arriba en importancia real.

### `study_work_stall_risk`
Dispara con 2+ de: proyecto In Progress sin próxima acción física · tarea pateada 2 veces · más de 3 tareas en un día · bloques de estudio/trabajo ausentes de la semana.
**Acción**: definir UNA próxima acción física para el proyecto trabado, o mover el excedente de tareas a otro día. En v2 esta señal vigila también los bloques de estudio.

## Orden de evaluación

- **Prioridad predictiva** (orden en que se chequean): energía → plata → casa → comida/suplementos → estudio/trabajo.
- **Importancia real** (cuál gana si disparan varias): plata → trabajo → comida/suplementos.
- Máximo **una señal comunicada por interacción** — la más importante. Las demás esperan; el sistema no abruma.

---

Parte del [[Agentic OS PRD]] · datos: `vault/Raw/life-signals/` + Notion + [[Morning Gate]]
