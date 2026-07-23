---
categories: [reference]
subjects: [finanzas, dataviz]
status: active
---

# Spec del dashboard HTML del cierre mensual

Refinada del sketch original. El objetivo no es un resumen lindo: es una herramienta de análisis visual que responde en la primera pantalla ¿mejor o peor?, ¿cuál de los 3 números importa este mes?, ¿cuál es LA acción?

**Referencia viva**: `Dashboards/TEMPLATE.html` es el esqueleto de referencia — copiarlo y reemplazar datos/lecturas es el camino, no rediseñar de cero. El índice histórico es `index.html` (cada cierre agrega su fila arriba del comentario marcado).

## Reglas no negociables

1. **Cargar la skill `dataviz` ANTES de escribir cualquier gráfico** — forma primero, color último, paleta de referencia ya validada (secuencial azul, divergente azul↔rojo, status reservados), dark mode con `prefers-color-scheme`.
2. **Autocontenido**: CSS/JS inline, cero CDN, cero internet. Gráficos en HTML/CSS (barras, progress, delta) o SVG inline; nada de Chart.js/D3 remotos, tortas, donuts, gauges ni 3D.
3. **Cada gráfico responde una pregunta y tiene una frase de lectura.** Si no cambia una decisión, no va.
4. **No exponer movimientos completos** — solo agregados y los ítems de "a revisar". Los datos sensibles no salen del vault.
5. **Comercios crípticos → tabla "a revisar", nunca adivinar.**

## Formas según historia disponible

- 2-3 cierres: stat tiles con delta, barras horizontales pareadas (mes vs anterior), barras divergentes para variación, progress para el plan.
- 4+ cierres: se agregan sparklines en las KPI y línea mensual de los 3 números. No antes.

## Estructura (secciones en orden)

1. **Header**: mes, nav índice/anterior/siguiente, frase principal del mes (la historia en 2 líneas).
2. **Panel de control**: 4 stat tiles — revolving (meta $0), plan de deuda, delivery, gasto real total. Cada una: valor, delta vs mes anterior, lectura corta, dirección deseada como tag.
3. **Qué cambió**: barras divergentes por categoría (rojo=subió, azul=bajó), marcando qué es puntual y qué es hábito.
4. **Dónde se fue la plata**: barras horizontales ordenadas, mes actual + anterior de referencia (ghost), top 8 + otros.
5. **La palanca**: progress del plan (cuota N/24, estado: activo/consultado/precancelado, interés restante).
6. **Lo que estoy aprendiendo**: 4 bloques con números (funcionó / necesita ajuste / ruido / seguimiento).
7. **A revisar**: tabla priorizada (ALTA/MEDIA/BAJA) — separada de patrones confirmados.
8. **Hacer, no pensar**: UNA acción — por qué, primer paso físico, tiempo, guion listo, métrica que mejora, cómo se verifica el próximo cierre. La acción además se carga a Notion (regla 5b del sistema).
9. **`<details>` de fórmulas**: qué mide cada métrica, fuente, qué excluye, dirección.

## Métricas — capa antes que gráficos

Núcleo (tablero): revolving, plan, delivery. Diagnóstico: gasto real total, por categoría, variación m/m, top subas/bajas. Comportamiento: puntual vs hábito. **Métrica de acción**: la que mejora si la usuaria hace LA acción del mes (se nombra explícita en la sección 8.

## Validación antes de terminar

Métricas con fórmula clara · cada gráfico responde una pregunta · nada decorativo · sin movimientos completos · funciona sin internet · nav índice/anterior/siguiente · abrir en browser y mirar (sin solaparse, sin overflow horizontal) · fila nueva en index.html.
