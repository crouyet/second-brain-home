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

Para cada producto de `productos.json`, aplicá esta lógica. Modelo completo en
[[../Sistema/Modelo de estado de la cocina]].

### 1. Estado de stock

Cada producto tiene `estado` + `estado_desde` — no un campo de stock en texto libre, que
mezcla estado, cantidad y razón, y hace que cada agente lo interprete distinto.

| `estado` | Qué hacer |
|---|---|
| `agotado` | va a la lista **si su `rol` lo justifica** (ver abajo). 🔴 con `urgencia: alta`, si no 🟡 según el mapa de días |
| `bajo` | va a 🟡 — alcanza para poco, no es emergencia |
| `pedido` | **ignorar**: ya está resuelto, no reordenar |
| `pausado` | ignorar: decisión explícita de no reponer |
| `disponible` | 🟢, no se compra |
| `desconocido` | nunca se registró — **no asumir nada**: si el menú lo necesita va a la pregunta, si no se ignora |

### 1b. `origen` — antes que cualquier otra cosa

Un producto con `origen: cocinado` **no se compra nunca: se cocina.** Son el piso de comida
lista (verduras cortadas, algo para picar, caldo, legumbre cocida). `/compras` los **ignora
por completo** — no tienen comercio. Cuando uno se vence, el gap lo levanta `/chefcito` como
paso del bloque de prep. Si uno aparece en una lista de compras, es un bug.

### 1c. `rol` — cómo se consume, y por eso si entra a la lista

| `rol` | Un `agotado` de este rol… |
|---|---|
| `constante` | **va a la lista siempre.** Si no está, falta — es la base de la cocina |
| `rotacion` | **va a la lista** según el mapa de días. El ciclo normal de reposición |
| `esporadico` | **NO va a la lista por sí solo.** Solo si una receta de la semana lo pide |

Un `esporadico` no se compra porque falte: se compra **si una receta lo pide y si ese día
tiene buena pinta**. Es una decisión subjetiva en el momento, no una reposición. Meterlo en
la lista por estar `agotado` la llena de cosas que no se pensaban comprar, y **una lista con
ruido se deja de leer**.

### 1d. `dudoso` — se calcula, no se guarda

Significa "hay que confirmarlo para poder decidir", y **depende del `rol`**: no todo envejece
igual.

| `rol` | Cuándo es dudoso |
|---|---|
| `rotacion` | `hoy - estado_desde > tolerancia_dias` |
| `constante` | **solo si nunca se registró.** Que tengas sal no caduca a los 30 días: cambia por un evento, no por el almanaque |
| `esporadico` | solo si nunca se registró, y aun así entra a ❓ únicamente si el menú lo necesita |

Sin `estado_desde` → dudoso en los tres casos. Sin campo `rol` → asumir `rotacion` (default
seguro: pregunta de más, nunca de menos). Esto reemplaza la vieja regla fija de ">45 días",
que trataba igual a la sal y al pescado fresco.

- Un `agotado` **dudoso** NO infla la lista 🔴 — puede haberse comprado sin registrar: va a ❓.
- Un `pedido` **dudoso** es un **pedido fantasma**: puede haber llegado sin registrarse, o el
  pedido nunca haberse hecho. Va a ❓ con la pregunta correcta — *"¿el pedido de X ya llegó o
  sigue pendiente?"*, no "¿te falta X?". **Nunca dejarlo en silencio**: `pedido` hace que el
  producto se ignore, y un producto ignorado indefinidamente desaparece del sistema.
- Los `constante`/`esporadico` nunca registrados **no entran a la rotación semanal**: son un
  barrido de inventario de una sola vez, aparte de la lista. Meterlos ahí tapa los
  perecederos, que es lo único que cambia semana a semana.

### 1e. Transiciones que le corresponden a `/compras`
Cada cambio actualiza `estado_desde`:

1. **`agotado` → `pedido`** al volcar el producto a una tarea de comercio. Sin esto vuelve a
   la lista todas las semanas aunque ya esté encargado.
2. **`pedido` → `disponible`** cuando la tarea pasa a Done; si la descripción dice que no se
   consiguió → vuelve a `agotado`.
3. Si la usuaria dice que algo llegó o que nunca lo pidió, **gana su palabra**.

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

### ❓ ¿Sigue faltando? (máx 5 ítems, numerada)
Los `dudoso` de rol `rotacion`: los que el menú necesita + 1-2 de rotación (los más viejos).
**Nunca más de 5** — una lista de 30 no se contesta, y una lista sin contestar es peor que no
preguntar, porque deja datos viejos disfrazados de nuevos. Se responde con números:

```
1) Pescado  2) Dátiles  3) Almendras  4) Tomate
Decime los números de lo que SÍ tenés. Lo que no menciones lo doy por agotado.
```

**El default del silencio es el seguro**: lo que no se menciona se marca agotado, nunca
disponible. La respuesta actualiza `productos.json` vía modo registrar.

### 🟢 Ya tenés / esperá
Una línea por producto, sin detalle.

## Reglas generales
- Verificá descuentos vigentes antes de sugerir dónde comprar.
- Cada ítem de la lista sale de una necesidad/receta concreta — no comprar fresco que no
  entre en ningún plan de la semana.
- Sé concisa. Una decisión clara vale más que cuatro opciones.
