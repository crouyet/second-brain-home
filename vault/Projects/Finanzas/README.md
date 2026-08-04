---
categories: [project-brief, index]
subjects: [finanzas]
status: active
---

# Finanzas Personales (EJEMPLO — módulo opcional)

> Activalo en `config.md`. Análisis mensual de resúmenes bancarios: buscar patrones de
> gasto, detectar dónde optimizar, ayudar a mejorar la salud financiera.

## Cómo funciona

1. Subís el **Excel/PDF de movimientos** del mes a `Resumenes/` (el detallado, uno por
   tarjeta/cuenta — ver formato de nombre en `Resumenes/README.md`).
2. Al analizar: se excluyen intereses/impuestos/reversas del cálculo de "gasto real", se
   categoriza cada movimiento (delivery, transporte, restaurantes, suscripciones, etc.) con
   `comercios.json`, y se compara contra el análisis del mes anterior en este mismo archivo.
3. Se genera un `.md` nuevo tipo `Analisis <periodo>.md`: comparación mes a mes, patrones
   (qué subió, qué bajó, en qué categoría se gasta más), y sugerencias concretas con los
   números reales detrás.

## Análisis

*(vacío — acá se va a listar cada `Analisis <periodo>.md` a medida que corras
`/cierre-finanzas`)*

## Notas
- Los archivos de `Resumenes/` son información sensible (movimientos bancarios) — no
  se comparten fuera de este análisis.
- Comercios con nombre críptico o montos grandes quedan marcados "a revisar" en vez de
  adivinar qué son.
- Anotá acá cualquier punto ciego conocido de tu propio caso (ej. un medio de pago que no
  pasa por resumen bancario y por lo tanto el análisis nunca ve).
