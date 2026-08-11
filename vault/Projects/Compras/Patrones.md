---
categories: [permanent-note]
subjects: [compras, finanzas, patrones]
status: active
actualizado: <fecha de la última vez que lo minaste>
---

# Patrones de compra reales (EJEMPLO — llenalo con los tuyos)

> Lo que **de verdad** comprás, minado de tus resúmenes bancarios — no lo que creés que
> comprás. `/compras` lo usa como realidad de fondo; [[instrucciones]] tiene las reglas
> operativas. Se re-mina en cada cierre financiero, no todas las semanas.

## Cómo se llena

Los resúmenes de `../Finanzas/Resumenes/` son la única fuente que **no depende de que te
acuerdes de registrar nada**. De ahí salen tres cosas por comercio: cada cuánto comprás,
cuánto gastás típicamente, y qué día de la semana caés. Eso corrige las `frecuencia` de
`productos.json`, que al principio son estimaciones tuyas y casi siempre están mal.

Ojo con una trampa: los resúmenes son **por comercio, no por producto**. Saber que gastaste
en el súper no te dice qué compraste. No inventes `ultima_compra` de un producto porque
apareció el comercio.

## Lo que las tarjetas SÍ muestran

| Patrón | Evidencia | Implicancia operativa |
|---|---|---|
| {{comercio}} cada ~N días, ~$X | N cargos en M meses | ajustar `frecuencia` de esos productos |
| {{comercio}} siempre el mismo día | los cargos caen todos el mismo día de semana | es tu proveedor de facto: planificá ese bloque ahí |
| Suscripciones que no recordabas | cargos mensuales iguales | revisalas: es la plata más fácil de recuperar |

## El punto ciego — importa más que lo de arriba

**Todo lo que pagás en efectivo o por transferencia es invisible acá.** Ferias, puestos,
verdulerías, pedidos por mensaje, lo que le comprás a alguien directo. Para esos comercios
los resúmenes no sirven y **el modo registrar (`/compras registrar`, o dictarlo por
Telegram) es la única fuente de verdad**.

Consecuencia práctica: si un producto vive en un comercio del punto ciego, su
`estado_desde` **solo se actualiza si lo registrás vos**. Por eso esos productos se vuelven
`dudoso` seguido y aparecen en la pregunta semanal — no es un bug del modelo, es que
literalmente nadie más vio esa compra.

## Qué hacer con esto

1. Corregir `frecuencia` en `productos.json` donde el resumen contradiga tu estimación.
2. Anotar acá los comercios del punto ciego, para saber cuáles dependen de tu registro.
3. **No tocar `ultima_compra`** salvo que el resumen pruebe la compra de ese producto.
