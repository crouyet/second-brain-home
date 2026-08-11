---
categories: [project-brief]
subjects: [chefcito, cocina]
status: active
---

# Chefcito (EJEMPLO)

> Módulo opcional. `/chefcito` arma meal prep accionable desde tu inventario real y
> planifica la semana **dimensionada contra tu estructura de comidas**, no contra la de
> otro. (Contenido personal — no lo compartas si no querés.)

**[[CONTEXT]] — el contrato del agente: qué lee, qué escribe, y la frontera con Compras.
Leer primero.**

## El modelo de planificación que trae el repo es UN ejemplo

`Planes Semanales/_template.md` viene con la estructura de quien escribió el sistema.
**`/setup` te pregunta cómo armás vos el menú** — cuántas veces comés, cuáles cocinás y
cuáles resolvés con lo que haya, quién cocina y qué días — y reescribe el template con eso.
Si nunca corriste el setup, editalo a mano.

Lo único que conviene no tocar, porque es lo que evita que el plan se quede corto:

1. **Declarar la demanda antes de elegir recetas** — cuántas comidas tiene que cubrir la semana.
2. **Declarar cuántas porciones rinde cada bloque** de cocina.
3. **Producción ≥ demanda** antes de dar el plan por bueno.

## Qué poné acá

- `Recetas/` — tu biblioteca. Cada receta declara `funcion: [tag, tag]` en el frontmatter:
  de ahí sale la cobertura funcional que calcula `tools/chefcito/cobertura.py`.
- [[Plan-nutricional]] — tus 3 niveles (fijas / rotación / novedad) y tu piso funcional.
- [[Banco de Snacks]] — el piso de comida lista, con cuánto dura cada preparación.
- `Inventario.md` — el estado real de heladera, freezer y despensa.
- Preferencias, alergias, intolerancias, y el equipamiento que **no** tenés (para que no te
  sugiera recetas que no podés hacer).
