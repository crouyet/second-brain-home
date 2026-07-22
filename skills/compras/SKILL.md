---
name: compras
description: Shopping Cycle completo de la usuaria — qué comprar, dónde, cuándo y con qué descuento; y modo registrar para retroalimentar productos tras cada compra. Usar cuando diga /compras, feria, lista de compras, o quiera registrar lo comprado.
model: haiku
effort: low
---

**Nivel de riesgo**: modo lista = Nivel 2 (1 review de la-contadora antes de mandarla) · modo registrar = Nivel 1 (actúa sola). Ver [[Contrato de autonomía]].

Seguí al pie de la letra `vault/Projects/Compras/instrucciones.md` (el system prompt completo: lugares, motor de decisión, formato 🔴🟡🟢) con `vault/Projects/Compras/productos.json` como fuente de verdad de productos y **`vault/Projects/Compras/Descuentos y medios de pago.md` como fuente de verdad de medios de pago y descuentos — lectura OBLIGATORIA antes de cualquier lista** (qué medios tiene → qué descuentos aplican → qué día conviene → dónde conviene precio/calidad). Al verificar descuentos online, **actualizá ese registro** (columna `verificado`, vencidos, nuevos, frontmatter `actualizado:`) — es un registro vivo, cada corrida lo deja más fresco. La feria es UN comercio del ciclo (varios puestos que comparten tope Buepp), no el todo. En Notion, el proyecto [Shopping Cicle](https://app.notion.com/1db6b0ad2b06800babf1cd5ebced2f3f) agrupa las tareas de compra (base Tareas `collection://{{TAREAS_COLLECTION_ID}}`, templates por comercio y tags de descuento tipo "Martes 30%").

## Modo lista (default)
Aplicá el proceso de instrucciones.md. Antes de armar la lista, revisá también la nota "Compras por registrar" si la usuaria la menciona (dictados del atajo 🎤) y las tareas abiertas del Shopping Cicle en Notion.

## Modo registrar (después de comprar)
Por cada producto comprado, actualizá **en `productos.json` Y en `Productos.md`** (son la misma lista, mantener sincronizados):
- `ultima_compra` → fecha de hoy · `stock_actual` → "ok" · precio pagado y lugar si cambió · link si hay uno nuevo.
- Producto nuevo → agregarlo con el esquema existente (lugar, frecuencia, umbral_calidad, etc.).
- Descuento vencido o nuevo detectado → actualizar la sección de medios de pago de `instrucciones.md` y avisarle.
- Cerrá la tarea correspondiente en Notion si existe.

Este loop es el corazón: con `ultima_compra` + `frecuencia`, la próxima lista estima reposición sola — cada compra registrada hace al agente más preciso.

**Regla 5b del sistema**: si de cualquier modo sale un accionable con próxima acción física clara que no sea la compra misma (ej. "reclamar un descuento mal cobrado", "pedir presupuesto a X"), se carga a Notion vía `/planificar` en el momento — no queda solo en un .md. No duplicar tareas ya abiertas.
