---
categories: [permanent-note]
subjects: [sistema, hestia, confianza]
status: active
---

# Trust ledger

Historial de confianza por capacidad. Tiers: **watch** (recién nace, se observa) →
**queue** (pide 1 review, Nivel 2 del [[Contrato de autonomía]]) → **auto** (actúa sola).
Gradúa con 10 corridas ≥90% de aprobación; degrada automático si cae <80%. Todo arranca
en `queue` salvo el tick de la mañana (`auto` desde el día 1 — solo informa, no compromete
nada).

Arranca vacío — `/revision` lo va llenando semana a semana con lo que corrió de verdad.

## Capacidades

| Capacidad | Corridas | Aciertos | % | Tier |
|---|---|---|---|---|
| Tick de la mañana (energy_forecast) | 0 | — | — | auto |
| Lista de compras (veredicto la-contadora) | 0 | 0 | — | queue |
| Mejora semanal (`/revision`, veredicto la-veterana) | 0 | 0 | — | queue |

`/revision` actualiza esta tabla cada semana con lo corrido esa semana.

## Predicciones

Cada corrida del tick de la mañana appendea una fila acá (energía predicha vs. lo que la
usuaria reportó, si tocó un botón de check-in). Sirve para ajustar [[Energia]].

| Fecha | Energía predicha | Por qué | Reportada |
|---|---|---|---|
