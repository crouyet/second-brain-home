---
fecha: {{fecha de la corrida, YYYY-MM-DD}}
semana: {{del}} al {{al}}
categories: [meal-prep]
subjects: [cocina]
status: active
---

# Plan semana {{d/m}}

> ## ⚠️ Esto es UNA forma de armar el menú, no LA forma
>
> El template viene con la estructura de quien escribió el sistema: 5 tomas por día, dos
> personas cocinando, la proteína como eje. **La tuya casi seguro es otra.** `/setup` te
> pregunta cómo armás vos el menú y reescribe este archivo con tu estructura — columnas,
> bloques, quién cocina. Si ya corriste el setup y esto sigue igual, editalo a mano.
>
> **Lo que sí es genérico y conviene no tocar** — es lo que evita que el plan se quede corto:
> 1. **Declarar la demanda ANTES de elegir recetas** (sección 1b).
> 2. **Declarar cuántas porciones rinde cada bloque** (sección 3).
> 3. **Que producción ≥ demanda** antes de dar el plan por bueno.
>
> Cuántas tomas, quién cocina y qué días: eso es tuyo.

## 1. Contexto (el análisis, antes de decidir nada)

| Señal | Estado esta semana | De dónde sale |
|---|---|---|
| **Stock crítico** | qué se pone feo primero → se usa YA | `Inventario.md` |
| **Rotación** | qué proteína/base toca, para no repetir | planes de las últimas 2 semanas |
| **Quién cocina** | qué días y quién | `../../Sistema/config.md` |
| **Excepciones** | viaje, feriado, semana sin ayuda, indisposición | tu calendario |
| **Señales opcionales** | energía, entrenamiento, ciclo — solo si las activaste | `config.md` |

**Resumen en 2 líneas**: {{qué condiciona esta semana y qué se prioriza}}

> **Chequealo, no lo asumas**: ¿hay feriado o viaje? ¿qué día viene quien te ayuda? Si el
> día no está confirmado, **no lo inventes**: usá una regla relativa ("el día que venga se
> cocina X, los 2 siguientes se come Y"). Un plan que depende de un supuesto sin confirmar
> se cae entero.

## 1b. La demanda de la semana (aritmética, antes de elegir recetas)

Cuánta comida hace falta. **Se calcula, no se estima** — un plan que cubre una sola comida
al día y no suma es cómo se queda corto sin que nadie se dé cuenta.

| Toma | Tipo | Días que aplica | Total semana |
|---|---|---|---|
| {{tu toma 1}} | **preparación** / **stock** | {{}} | {{N}} |
| {{tu toma 2}} | | | {{N}} |
| {{tu toma 3}} | | | {{N}} |

- **Preparación** = hay que cocinarlo, sale de los bloques de la sección 3.
- **Stock** = no se cocina, se garantiza que esté (ver `../Plan-nutricional`).

**Totales**: {{X}} tomas de preparación · {{Y}} de stock.
**Objetivo nutricional** (si lo definiste en `config.md`): {{objetivo × días = total semana}}.
Si no tenés uno, saltá esta línea — el plan sale igual, solo sin dimensionar contra un número.

## 2. Recetas de la semana y su función

| Receta | Función nutricional | Quién / cuándo |
|---|---|---|
| [[receta]] | qué aporta | {{quién la hace y qué día}} |

Nivel 1 (fijas) · Nivel 2 (2-3 en rotación) · Nivel 3 (1 nueva). Ver [[../Plan-nutricional]].

**Cobertura funcional** (`python3 tools/chefcito/cobertura.py <slugs>`): {{pegar la salida —
qué cubre, qué no llega al piso, y a qué función apunta la receta nueva}}

## 3. Bloques de cocina

**Cada paso declara cuántas porciones rinde.** Sin ese número no se puede saber si la
semana alcanza, que es exactamente por qué se queda corta.

**{{Bloque 1 — quién, qué día}}** (~{{X}} min). Pasos chicos, en orden operativo:
1. {{acción física concreta}} → {{dónde queda}} — **{{N}} porciones**
2. {{"mientras tanto" — aprovechar los tiempos muertos}} — **{{N}} porciones**

**{{Bloque 2, si hay alguien más cocinando}}**: lo que lleva horno y tiempo va acá.

**Micro-prep la víspera** (2 min): bajar del freezer lo del día siguiente.

**Producción total**: {{suma de porciones}} contra {{X}} tomas de preparación de 1b.
Si no llega, **escalar una receta o sumar un bloque acá** — no dar el plan por bueno corto.

## 4. Las tomas, día por día

Solo lo que decidís plato por plato va con nombre de receta. El resto se llena con **qué
stock lo cubre**. **Una celda vacía es el bug**: significa que ese día, a esa hora, no hay
nada.

| Día | {{toma 1}} | {{toma 2}} | {{toma 3}} |
|---|---|---|---|
| Lun | | | |
| Mar | | | |
| Mié | | | |
| Jue | | | |
| Vie | | | |

## 4b. Efecto esperado — se aplica SOLO con el Done del bloque

Qué consume este plan. **Es una declaración, no un cambio**: mientras la tarea del bloque no
esté Done, ningún producto se toca (ver [[../../Sistema/Modelo de estado de la cocina]]).

| Bloque | Producto (`productos.json`) | Efecto |
|---|---|---|
| {{bloque}} | {{nombre exacto en productos.json}} | `agota` / `baja` |

- `agota` → `estado: agotado` · `baja` → `estado: bajo`. Ambos con `estado_desde` = fecha del Done.
- Ante la duda, `baja`: degradar de menos es más barato que recomprar de más.
- **Comida cocinada de este plan: default `agota`, no se declara acá.** Si no decís que
  quedó, no hay.

## 5. Compras que dispara este plan

**Chefcito no asigna comercio** — solo detecta:
- Staples habituales → marcados en `productos.json` (`estado`/`estado_desde`/`urgencia`)
- Puntuales de receta → sección de faltantes de `Inventario.md`

`/compras` decide dónde y cuándo. Ver [[../../Compras/CONTEXT]].

> **Lo que se cocina esta semana sale de lo que YA está en la cocina.** Lo que se compra
> ahora alimenta la semana **siguiente**. No planifiques recetas cuyos ingredientes todavía
> están en la lista de compras.

## 6. Al cerrar

- [ ] Demanda (1b) calculada, y **producción ≥ demanda** en tomas de preparación
- [ ] Ninguna celda vacía en la tabla de tomas (sección 4)
- [ ] Efecto esperado (4b) declarado para cada bloque
- [ ] Propuesta mandada y aprobada — **antes no se publica nada**
- [ ] Bloques de cocina como tareas, con los pasos en la descripción
- [ ] Gaps volcados a `productos.json` / faltantes de `Inventario.md`
