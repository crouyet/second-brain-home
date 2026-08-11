---
name: compras
description: Shopping Cycle completo de la usuaria — qué comprar, dónde, cuándo y con qué descuento; y modo registrar para retroalimentar productos tras cada compra. Usar cuando diga /compras, feria, lista de compras, o quiera registrar lo comprado.
model: haiku
effort: low
---

**Nivel de riesgo**: modo lista = Nivel 2 (1 review de la-contadora antes de mandarla) · modo registrar = Nivel 1 (actúa sola). Ver [[Contrato de autonomía]].

**Leé primero `vault/Projects/Compras/CONTEXT.md`** — tu contrato: qué leés, qué escribís, y la frontera exacta con Chefcito.

**No leas `productos.json` ni `Productos.md` enteros**: de un catálogo entero usás solo lo que falta. Corré la proyección, que trae exactamente eso:

```bash
python3 tools/compras/regenerar-productos-md.py --para compras
```

Te da qué falta agrupado por comercio con las urgencias (⚠️) y los candidatos a la pregunta de confirmación. **Ya viene filtrada**: sin `rol: esporadico` y sin `origen: cocinado`. Si necesitás un dato que la proyección no trae (precio, link), buscá ese producto solo.

Seguí al pie de la letra `vault/Projects/Compras/instrucciones.md` (el motor completo: lugares, urgencia → día, calidad/precio, formato 🔴🟡🟢) — **eso sí entero, es criterio, no datos** — y **`vault/Projects/Compras/Descuentos y medios de pago.md` como fuente de verdad de medios de pago y descuentos: lectura OBLIGATORIA antes de cualquier lista** (qué medios tiene → qué descuentos aplican → qué día conviene → dónde conviene precio/calidad). Al verificar descuentos online, **actualizá ese registro** (columna `verificado`, vencidos, nuevos) — es un registro vivo, cada corrida lo deja más fresco. En el backend de tareas, un proyecto de compras agrupa las tareas (base Tareas `collection://{{TAREAS_COLLECTION_ID}}`, templates por comercio).

## Modo lista (default)

**Paso 0 — Reconciliación (el estado vive en la tarea):** mirá las tareas de compra completadas en los últimos 14 días. Una tarea Done marca que la compra se hizo, pero **lo efectivamente comprado se lee de su descripción**: de lo planificado puede haber cosas que no llegaron, y esas siguen pendientes. Por cada producto que la descripción confirme, actualizá en `productos.json`: `ultima_compra`, `estado: disponible` y `estado_desde` = la fecha del Done (solo si es más nueva que la registrada — correrlo dos veces no cambia nada).

**Regla dura inversa: una tarea que sigue ABIERTA es NO comprada.** Jamás asumas comprado algo cuya tarea no está Done; re-entra a la lista.

Después aplicá el proceso de `instrucciones.md` para armar la lista.

## Modo registrar (opcional — detalle fino)

El registro canónico de "comprado" es la tarea Done (paso 0). Este modo corre cuando la usuaria quiere dejar detalle (precio pagado, producto nuevo) o responder la pregunta de confirmación. Por cada dato:

- Actualizá **solo `productos.json`** (única fuente que se edita): `ultima_compra` → hoy · `estado` → `disponible` con `estado_desde` de hoy · precio y lugar si cambiaron.
- Producto nuevo → agregarlo con el esquema completo, **incluido `rol`** (`constante` / `rotacion` / `esporadico`) y `origen`. Sin `rol` se asume `rotacion`, que es el default seguro.
- Al final, **regenerá `Productos.md` corriendo `python3 tools/compras/regenerar-productos-md.py`** — no lo escribas vos. Es un artefacto generado: escribirlo a mano pierde marcadores en silencio.

Este loop es el corazón: con `ultima_compra` + `frecuencia`, la próxima lista estima reposición sola.

**Regla 5b del sistema**: si de cualquier modo sale un accionable con próxima acción física clara que no sea la compra misma (ej. "reclamar un descuento mal cobrado"), se carga como tarea vía `/planificar` en el momento — no queda solo en un `.md`. No duplicar tareas ya abiertas.
