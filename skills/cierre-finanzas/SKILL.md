---
name: cierre-finanzas
description: Cierre financiero mensual de la usuaria — analiza los resúmenes nuevos de Resumenes/, compara contra la historia y actualiza el tracker de 3 números. Usar cuando diga /cierre-finanzas, cierre del mes, o suba resúmenes nuevos.
model: sonnet
effort: medium
---

**Nivel de riesgo**: Nivel 1 (actúa sola) para el análisis y el tablero; cualquier decisión de plata >$50.000 (ej. precancelar deuda) sube a Nivel 3 (consejo completo). Ver [[Contrato de autonomía]].

Flujo definido en `vault/Projects/Finanzas/README.md` (leer primero); tablero y roadmap en `vault/Projects/Finanzas/Plan.md`; historia en los `Analisis *.md` existentes.

1. Detectá los archivos nuevos en `vault/Projects/Finanzas/Resumenes/` (Excel de movimientos, uno por tarjeta).
2. Corré `tools/finanzas/categorizar.py` (necesita xlrd: `python3 -m venv .venv && .venv/bin/pip install xlrd` la primera vez). Ya resuelve lo mecánico: excluye financiero/impuestos, netea reversas (incluido el caso cargo/devolución con nombres distintos), descarta ecos duplicados de planes de cuotas refinanciados, categoriza con `vault/Projects/Finanzas/comercios.json` y chequea las alertas que hayas definido ahí (ej. un seguro o suscripción que aparezca con un cargo neto inesperado → avisar que hay que reclamar). No re-implementes nada de eso a mano.
2b. Los "sin clasificar ≥$15k" de la salida: resolvelos con la usuaria (o marcálos "a revisar") y **agregá lo resuelto a comercios.json** — el diccionario aprende, el sistema no pregunta dos veces (regla 7).
3. **Actualizá el tablero de `Plan.md`**: interés revolving (¿sigue $0?), la cuota de tu plan de deuda/refinanciación si figura uno en `Plan.md` (¿avanzó una cuota? ¿bajó el interés? ¿se precanceló?), y el gasto que estés vigilando ese mes (ej. delivery: ¿está bajando?).
4. Escribí `Analisis <periodo>.md` nuevo (mismo formato: resumen ejecutivo, tabla mes a mes, hallazgos, "a revisar", próximos pasos) y actualizá la lista de análisis del README.
4b. **Dashboard HTML**: generá `Dashboards/<periodo>.html` siguiendo `vault/Projects/Finanzas/Dashboard spec.md` (leerla entera; cargar la skill `dataviz` antes de cualquier gráfico; `Dashboards/2026-06.html` es el template real — copiar y reemplazar datos/lecturas). Agregá la fila del cierre en `index.html` (arriba del comentario marcado) y el link "mes siguiente" en el dashboard del mes anterior. Verificá abriéndolo en el browser.
5. Cerrá con 3 líneas para la usuaria: los 3 números, un win, y LA acción del mes (una sola).
6. **Regla 5b del sistema**: si LA acción del mes tiene próxima acción física clara, cargala a Notion vía `/planificar` antes de cerrar (salvo que ya exista una tarea abierta con esa misma acción — no duplicar). No queda solo en el .md.

Sensible: el contenido de `Resumenes/` no sale de este análisis. Comercios crípticos → "a revisar", nunca adivinar.
