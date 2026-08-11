# Compras — contrato del agente

One job: decidir **qué entra a tu cocina** — qué falta, dónde conviene comprarlo, qué día y
con qué medio de pago. No decide qué se cocina.

## Inputs
- Working: `productos.json` — la fuente de verdad del estado de cada producto. **No lo leas
  entero**: corré `python3 tools/compras/regenerar-productos-md.py --para compras`, que
  emite solo lo que falta, agrupado por comercio (dos órdenes de magnitud menos de texto).
- Reference: `instrucciones.md` (el motor: lugares, urgencia → día, calidad/precio),
  `Descuentos y medios de pago.md` (registro vivo, lectura obligatoria antes de una lista).
- Reference: `../Sistema/Modelo de estado de la cocina.md` — qué significa cada estado.
- Del backend de tareas: las compras completadas, para reconciliar qué se compró de verdad.

Do NOT load: `../Chefcito/` — qué se cocina no es tu trabajo. Lo único que cruza la frontera
son los faltantes que Chefcito deja anotados (ver abajo).

## Outputs
- `productos.json` — **la única fuente que editás**. Las transiciones que te corresponden:
  `agotado → pedido` (al volcar el producto a una tarea de comercio), `pedido → disponible`
  (cuando esa tarea pasa a Done), `pedido → agotado` (si la tarea cierra y no se consiguió).
- `Productos.md` — **generado**, nunca a mano: `python3 tools/compras/regenerar-productos-md.py`.
- Tareas de compra en tu backend, **una por comercio** — nunca una tarea genérica con ítems
  mezclados, porque la urgencia de cada ítem no es la misma.
- `Descuentos y medios de pago.md` — cada corrida lo deja más fresco.

## Human check
Nivel 2: la lista se muestra antes de comprar nada. **El botón de pagar es siempre tuyo** —
el sistema arma el carrito, vos confirmás. Ver `../Sistema/Contrato de autonomía.md`.

## Reglas que no se negocian
- **Tarea abierta = NO comprada.** Jamás dar por comprado algo cuya tarea no está Done.
- **Lo efectivamente comprado se lee de la descripción de la tarea**, no de lo que se
  planificó: puede haber cosas que no llegaron, y esas siguen pendientes.
- **`origen: cocinado` se ignora por completo** — eso se cocina, no se compra.
- **`rol: esporadico` agotado no entra a la lista solo** — solo si el menú lo pide.
- Si el usuario dice que algo llegó o que nunca lo pidió, **gana su palabra** sobre
  cualquier inferencia del sistema.

## Contrato con Chefcito
Compras decide **qué entra** (compra) y es dueño exclusivo de las tareas de compra;
Chefcito decide **qué se hace con eso** (menú) y qué falta. La frontera:

| | Compras puede | Compras NO puede |
|---|---|---|
| `productos.json` | las transiciones de arriba, precios, links, comercio | declarar efectos de un plan (eso es de Chefcito) |
| Tareas de compra | crear, actualizar, cerrar | — |
| Menú / plan semanal | leer si necesita saber qué se va a cocinar | escribir |
| `../Chefcito/Inventario.md` | leer la sección de faltantes puntuales | reescribir el inventario |

Ver `../Chefcito/CONTEXT.md` para el lado espejo.
