---
categories: [permanent-note]
subjects: [compras]
status: active
---

# Motor de compras (EJEMPLO — editá con tus locales y medios de pago)

> Esto es el "cerebro" completo de `/compras`: lugares, motor de decisión, formato de
> respuesta. La tabla de lugares y los descuentos son ficticios — reemplazalos con los
> tuyos. El motor (urgencia → timing → calidad/precio) es genérico, andá ajustándolo.

## Medios de pago

**Fuente de verdad: [[Descuentos y medios de pago]]** — registro vivo con tus medios de
pago, los descuentos por comercio (día, %, tope, vigencia) y la fecha de última
verificación. Leelo SIEMPRE antes de armar una lista.

**Regla:** los descuentos del registro son de referencia base — verificá vigencia real
antes de usarlos, y actualizá el registro con lo verificado.

## Lugares de compra (ejemplo)

| Lugar | Qué se compra | Frecuencia | Notas |
|---|---|---|---|
| Feria del barrio | Verduras, frutas | Semanal — día fijo | Descuento X% con tu billetera |
| Supermercado online | Despensa, limpieza | Cuando se necesite | Envío gratis con tu suscripción |
| Carnicería de confianza | Carne | Semanal | Proveedor de facto |

## Motor de decisión

Para cada producto de `productos.json`, aplicá esta lógica:

### 1. Urgencia de stock
- `stock_actual = "agotado"` o `urgencia = "alta"` → compra inmediata, ignorá precio.
- Si hay `ultima_compra`: si pasó más que `frecuencia_dias` → va a 🔴 o 🟡 según urgencia;
  si no, va a 🟢.
- **Regla de staleness**: un estado `agotado`/`urgencia alta` con más de 45 días sin una
  compra registrada que lo respalde es DUDOSO — no infla la lista, va a "¿Sigue faltando?"
  para que confirmes sí/no antes de tratarlo como urgente de verdad.

### 2. Timing — día de descuento
Cruzá urgencia × el mapa de días de descuento (mantenerlo consistente con
[[Descuentos y medios de pago]]):
- **Urgente de verdad**: HOY por el canal más rápido, aunque se pierda el descuento.
- **Reponer** (falta pero no quema): al próximo día de descuento del canal que corresponda.
- **Ir pensando**: se acumula hasta juntar 2-3 ítems del mismo canal — nunca un viaje/envío
  por un solo producto no urgente.

### 3. Calidad/precio
- `umbral_calidad: "alto"` → no cambiar de marca/proveedor por precio.
- `umbral_calidad: "medio"` → comparar si hay alternativa razonable.
- `umbral_calidad: "bajo"` → priorizar precio.

## Formato de respuesta — plan de semana

### 🔴 Comprá ahora
Producto → lugar → por qué ahora → medio de pago a usar.

### 🟡 Plan de la semana (agrupado por día)
> **Día X** — Local (descuento): productos.

### ❓ ¿Sigue faltando? (staleness, máx 5 ítems)
Estados dudosos (>45 días sin registro). Tu respuesta actualiza `productos.json` vía modo
registrar.

### 🟢 Ya tenés / esperá
Una línea por producto, sin detalle.

## Reglas generales
- Verificá descuentos vigentes antes de sugerir dónde comprar.
- Cada ítem de la lista sale de una necesidad/receta concreta — no comprar fresco que no
  entre en ningún plan de la semana.
- Sé concisa. Una decisión clara vale más que cuatro opciones.
