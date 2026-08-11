---
categories: [permanent-note]
subjects: [cocina, nutricion]
status: active
---

# Plan nutricional (EJEMPLO — adaptalo)

> Esto convierte "qué como" en "qué le doy a mi cuerpo". La **mecánica** (3 niveles,
> funciones como tags, piso semanal) es genérica; **los tags y los números son de ejemplo**.
> Si tenés objetivos de un profesional, ponelos en `../Sistema/config.md` — el planificador
> los lee de ahí, no de este archivo.

## Las funciones como tags

Cada receta de `Recetas/` declara qué aporta, en el frontmatter:

```yaml
funcion: [proteina-densa, hierro]
```

Los tags son tuyos. El set del ejemplo: `proteina-densa` · `omega-3` · `magnesio` ·
`calcio` · `hierro` · `zinc-cobre-b12` · `colageno-vitc` · `fibra-prebiotica` ·
`probiotico-fermentado` · `antiinflamatorio` · `antioxidante-polifenoles` ·
`carbohidrato-complejo`.

Sirven para dos cosas: elegir por función en vez de por antojo, y **medir la cobertura**
de la semana con `tools/chefcito/cobertura.py` en vez de estimarla a ojo.

Un combo no necesita tag propio: "mitocondrial" es la intersección de `magnesio` +
`omega-3` + `antioxidante-polifenoles`. Si una comida tiene los tres, ya está.

## Los 3 niveles

### Nivel 1 — Fijas (la columna vertebral)
No se piensan, se repiten. Son las que cubren tu base todas las semanas. Poné acá 3-5
recetas que ya hacés sin esfuerzo.

### Nivel 2 — Rotación (variedad moderada)
Un pool de 8-10 que se turnan de a 2-3 por semana, para no comer lo mismo pero tampoco
decidir de cero.

### Nivel 3 — Una nueva por semana (novedad)
**Cuál elegir no es libre: la decide el hueco de cobertura.** Correr
`python3 tools/chefcito/cobertura.py <recetas de la semana>` y apuntar a la función que no
llegue al piso. Así "ir sumando comidas funcionales" deja de depender de acordarse.

`--flojas` muestra qué funciones tienen menos recetas en tu biblioteca: ahí conviene sumar
recetas nuevas.

**Al graduar una receta al Nivel 2, dale de alta sus ingredientes en `productos.json`.**
Una receta que pasa a ser parte de tu dieta convierte a sus ingredientes en consumo
rutinario, y lo que no está en ese registro `/compras` **no puede reponer**: solo aparece
cuando ya te quedaste sin. Sin esta regla el agujero se reabre con cada receta nueva.

## El piso funcional de la semana

Vive en `PISO`, arriba de `tools/chefcito/cobertura.py`. **Editalo.** No es "una de cada
una": son las que si faltan dos semanas seguidas se notan.

## Cómo se usa en la práctica

1. Al planificar la semana: Nivel 1 fijo + 2-3 del Nivel 2 (sin repetir las últimas 2
   semanas) + 1 del Nivel 3 apuntado al hueco de cobertura.
2. **Chequeo de cantidad — es una resta, no una impresión.** El plan declara cuántas tomas
   necesita la semana y cuántas porciones producen los bloques. **Producción ≥ demanda antes
   de mandar la propuesta.** Si no llega: escalar una receta (cocinar 6 porciones cuesta lo
   mismo que 3) o sumar un bloque. Un plan que alcanza justo ya falló.
3. Si es una semana de poca energía: priorizar Nivel 1, bajar la exigencia de probar cosas
   nuevas (el Nivel 3 se salta, sin culpa).

## Lo que se abastece, no se programa

Hay comidas que no querés que te asignen plato por plato — las elegís en el momento. Para
esas, el trabajo de planificación es de **stock, no de menú**: que `productos.json` tenga
siempre esos ingredientes como `rol: constante`, para que `/compras` los reponga solo.

**Ojo con el matiz**: "no se programa" **no es lo mismo que "no se cuenta"**. El plan sigue
sin decidir qué desayunás el martes, pero sí tiene que **garantizar que haya con qué**. Una
celda vacía en la tabla de tomas no es libertad de elección: es que no hay comida.
