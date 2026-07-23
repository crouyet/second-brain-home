---
categories: [project-brief]
subjects: [compras]
status: active
---

# Compras (EJEMPLO — editá con tus locales)

> Módulo opcional. Activalo en `config.md`. La `/compras` skill decide qué comprar, dónde,
> cuándo y con qué descuento, a partir de `productos.json` (tu inventario) y tus locales/
> descuentos. Estos ejemplos son genéricos — poné los tuyos (los datos de negocio útiles no
> son personales, podés dejar los que te sirvan a vos y a otros).

## Cómo funciona
- `productos.json` — qué comprás, cada cuánto, stock actual, dónde conviene.
- Mapa de días de descuento (ej. "martes 30% en tal feria con tal tarjeta").
- La skill cruza staleness (¿se está por agotar?) con el día de descuento del canal.

## Modo registrar
Después de comprar, "compré X en Y $Z" actualiza `productos.json` (precio, fecha, stock).
