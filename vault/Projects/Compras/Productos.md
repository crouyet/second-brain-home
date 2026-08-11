---
categories: [reference]
subjects: [compras]
status: active
---

# Productos

Generado desde `productos.json` por `tools/compras/regenerar-productos-md.py` — **no editar a mano.** Modelo de estados en [[../Sistema/Modelo de estado de la cocina]].

🟢 disponible · 🟡 bajo · 🔴 agotado · 📦 pedido · ⏸️ pausado · ❔ desconocido · **?** = dudoso (hay que confirmarlo para poder decidir)

**El piso de comida lista** (`origen: cocinado`, sección Cocina) se repone **cocinando, no comprando**: cuando uno se vence entra al bloque de prep del domingo, nunca a la lista de compras.

**Rol** — cómo se consume, y por eso a quién se le pregunta: 🔁 constante (siempre está; solo cambia por un evento, no caduca con el tiempo) · 🔄 rotación (se consume dentro del ciclo; caduca a los `tolerancia_dias`) · 🎲 esporádico (se usa cuando una receta lo pide; se pregunta solo si el menú lo necesita)


## supermercado

| | Producto | Rol | Cantidad | Frecuencia | Desde | Notas |
|---|---|---|---|---|---|---|
| 🟢 | Sal | 🔁 |  | trimestral | 208d | constante: que tengas sal no caduca a los 30 días, cambia por un evento |
| 🔴 | Salsa picante | 🎲 |  | trimestral | 213d | esporadico: agotado NO va a la lista solo. Entra si una receta de la semana lo pide |
| ⏸️**?** | Algo que dejaste de comprar | 🔄 |  | mensual | 218d | pausado = decisión explícita de no reponer. Se ignora sin desaparecer del catálogo |

## feria

| | Producto | Rol | Cantidad | Frecuencia | Desde | Notas |
|---|---|---|---|---|---|---|
| 🔴**?** | Verdura de hoja | 🔄 | 1 atado | semanal | 203d | rotacion: perecedero real, el dato se vence rápido |
| 🟢**?** | Papa o boniato | 🔄 | 1kg | semanal | 205d | cada cuánto lo comprás y cuánto dura el dato son cosas distintas: se compra semanal, pero dura 3 semanas |

## carniceria

| | Producto | Rol | Cantidad | Frecuencia | Desde | Notas |
|---|---|---|---|---|---|---|
| 📦**?** ⚠️ | Proteína de la semana | 🔄 |  | semanal | 204d | pedido = ya está encargado, no reordenar. Si la fecha se pasa de tolerancia es un PEDIDO FANTASMA: va a la pregunta, nunca se ignora en silencio |

## tienda especializada

| | Producto | Rol | Cantidad | Frecuencia | Desde | Notas |
|---|---|---|---|---|---|---|
| ❔**?** | Especia de calidad | 🎲 |  | trimestral | nunca | desconocido = nunca se registró. NO es lo mismo que agotado: asumir que falta hace recomprar lo que ya tenés |

## Cocina

| | Producto | Rol | Cantidad | Frecuencia | Desde | Notas |
|---|---|---|---|---|---|---|
| 🔴 | Algo sano para picar | 🔁 |  | semanal | 203d | origen cocinado: NO va a la lista de compras nunca. Cuando se vence, sale como paso del bloque de prep. Es lo que evita terminar comiendo lo primero que aparece |
| ❔**?** | Verduras cortadas listas | 🔁 |  | semanal | nunca | la base para dejar la cena a 1 paso de armar el plato |
