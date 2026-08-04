---
categories: [permanent-note]
subjects: [compras, descuentos, finanzas]
status: active
actualizado: 2026-01-01
---

# Descuentos y medios de pago — registro vivo (EJEMPLO — editá con el tuyo)

> Fuente de verdad de con qué pagás y qué descuentos te aplican. `/compras` lo lee
> SIEMPRE antes de armar una lista, y lo actualiza cada vez que verifica. Tabla ficticia —
> reemplazala con tus tarjetas/billeteras y comercios reales.

## Tus medios de pago

| Medio | Notas |
|---|---|
| Tarjeta banco X | base de varios descuentos presenciales |
| Billetera digital Y | descuentos "comercios de cercanía" |
| Efectivo/QR | default sin descuento |

## Descuentos por comercio (ejemplo)

⚠️ = vigencia dudosa → reverificar antes de contar con él.

| Comercio | Descuento | Días | Tope | Verificado |
|---|---|---|---|---|
| Feria del barrio | 30% con billetera Y | Sábados | $X/mes | 2026-01-01 |
| Supermercado online | 25% con tarjeta X | Fin de semana | $X/mes | 2026-01-01 |
| Local de confianza | sin descuento fijo — calidad por sobre precio | — | — | — |

## Protocolo de verificación (lo ejecuta `/compras`, paso 1)
1. Chequear vigencia real de lo que se va a usar HOY (no todo el registro).
2. Actualizar `Verificado` con la fecha y corregir % / tope / días si cambió.
3. Descuento nuevo detectado → fila nueva + avisar.
4. Actualizar `actualizado:` del frontmatter.

## Historial de cambios
- 2026-01-01 — creación del registro (ejemplo, reemplazar con datos reales).
