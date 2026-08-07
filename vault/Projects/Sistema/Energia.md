---
categories: [permanent-note]
subjects: [sistema, hestia, energia, ciclo]
status: active
---

# Energia — heurística de energy_forecast

Parámetros que usa el tick de [[Mañana Hestia]] para predecir la energía del día. Sin ML:
son reglas ajustables acá, `/revision` las retoca con evidencia del [[Trust ledger]].

## Orden de confianza de las fuentes

1. `vault/Raw/health/*.json` (health-receiver, background confiable — el más reciente por `received_at`)
2. MCP `health-auto-export` (bonus, solo responde con la app abierta)
3. Bloques de hoy de "Peak Calendar" (conector)
4. Si nada responde: **media** (default, nunca preguntarle)

## Reglas de energía baja

- **Sueño**: <6h anoche → baja. El registro tiene que ser de la noche de ayer→hoy (chequeá la fecha, no tomes "el más reciente" a ciegas): el watch sincroniza cada ~5h y a las 8:30 puede no tener todavía la noche de anoche. Si el dato más nuevo es de una noche anterior, es que anoche no sincronizó aún — tratalo como **sin dato** (bajá un nivel en el orden de confianza), nunca como si ese número viejo fuera el de hoy.
- **Fase del ciclo** (desde el último flujo menstrual registrado):
  - Día 1-5: menstrual → **baja**
  - Día 6-13: folicular → media/alta
  - ~Día 14: ovulación → alta
  - Día 15+: lútea → media; **lútea tardía → baja**
- Cualquiera de las reglas de arriba que dispare, alcanza para marcar el día como baja
  (no hace falta que coincidan todas).

## Bloques de Peak Calendar

`brainFog` / `dip` → tratar como baja para esa franja. `morningPeak` / `eveningPeak` →
alta para esa franja. `windDown` → cierre del día, no asignar nada nuevo ahí.

## Ajuste

`/revision` retoca estos umbrales (ej. "<6h" → "<7h" si el patrón real lo pide) usando el
[[Trust ledger]] como evidencia — nunca a ojo.
