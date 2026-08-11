#!/usr/bin/env python3
"""Regenera Productos.md desde productos.json. Idempotente: correlo siempre que toques el json.

El .md es una proyección de lectura para Obsidian — la fuente es el json. Antes esto se
hacía a mano y las dos vistas derivaban (que es el mismo error que el modelo de estados
vino a arreglar). Ver vault/Projects/Sistema/Modelo de estado de la cocina.md
"""
import json
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parents[2] / "vault/Projects/Compras"
EMOJI = {"disponible": "🟢", "bajo": "🟡", "agotado": "🔴",
         "pedido": "📦", "pausado": "⏸️", "desconocido": "❔"}

HEADER = """---
categories: [reference]
subjects: [compras]
status: active
---

# Productos

Generado desde `productos.json` por `tools/compras/regenerar-productos-md.py` — **no editar a mano.** Modelo de estados en [[../Sistema/Modelo de estado de la cocina]].

🟢 disponible · 🟡 bajo · 🔴 agotado · 📦 pedido · ⏸️ pausado · ❔ desconocido · **?** = dudoso (hay que confirmarlo para poder decidir)

**El piso de comida lista** (`origen: cocinado`, sección Cocina) se repone **cocinando, no comprando**: cuando uno se vence entra al bloque de prep del domingo, nunca a la lista de compras.

**Rol** — cómo se consume, y por eso a quién se le pregunta: 🔁 constante (siempre está; solo cambia por un evento, no caduca con el tiempo) · 🔄 rotación (se consume dentro del ciclo; caduca a los `tolerancia_dias`) · 🎲 esporádico (se usa cuando una receta lo pide; se pregunta solo si el menú lo necesita)
"""


ROL = {"constante": "🔁", "rotacion": "🔄", "esporadico": "🎲"}


def dias(desde, hoy):
    """Días desde la última confirmación. None = nunca se registró."""
    if not desde:
        return None
    return (hoy - date.fromisoformat(desde)).days


def es_dudoso(p, d):
    """La confianza decae con el tiempo SOLO para lo que rota.

    Que tengas sal no caduca a los 30 días: la sal no se consume sola, cambia por un
    evento (se acabó, la usaste). Preguntar por rotación ahí es ruido que tapa lo que
    sí importa. Lo esporádico tampoco caduca — se pregunta cuando una receta lo pide,
    y eso lo decide /compras, no este render. Lo nunca registrado es dudoso siempre.
    """
    if d is None:
        return True
    return p.get("rol", "rotacion") == "rotacion" and d > p.get("tolerancia_dias", 45)


def render(productos, hoy):
    out = [HEADER]
    for lugar in dict.fromkeys(p.get("lugar", "—") for p in productos):  # orden del json
        out.append(f"\n## {lugar}\n")
        out.append("| | Producto | Rol | Cantidad | Frecuencia | Desde | Notas |")
        out.append("|---|---|---|---|---|---|---|")
        for p in (x for x in productos if x.get("lugar", "—") == lugar):
            d = dias(p.get("estado_desde"), hoy)
            marca = EMOJI.get(p["estado"], "❔") + ("**?**" if es_dudoso(p, d) else "")
            if p.get("urgencia") == "alta":
                marca += " ⚠️"
            nota = (p.get("notas") or "").replace("|", "\\|")
            if p.get("receta"):
                nota = f"[[{p['receta']}]] · {nota}" if nota else f"[[{p['receta']}]]"
            celdas = [marca, p["nombre"], ROL.get(p.get("rol", "rotacion"), "🔄"),
                      p.get("cantidad_habitual", ""),
                      p.get("frecuencia", ""), "nunca" if d is None else f"{d}d", nota]
            out.append("| " + " | ".join(celdas) + " |")
    return "\n".join(out) + "\n"


def proyeccion(productos, hoy, para):
    """Lo mínimo que cada agente necesita para decidir. ~250 tok contra ~10.300 del json.

    El agente NO lee productos.json ni Productos.md: lee esto. El json es el store, y el .md
    es la vista para Cami en Obsidian.
    """
    def marca(p):
        return " ⚠️" if p.get("urgencia") == "alta" else ""

    if para == "compras":
        # cocinado se repone cocinando; esporadico solo entra si el menú lo pide
        faltan = [p for p in productos if p["estado"] in ("agotado", "bajo")
                  and p.get("rol") != "esporadico" and p.get("origen", "comprado") != "cocinado"]
        out = [f"# qué falta ({len(faltan)}) — agrupado por comercio"]
        for lugar in dict.fromkeys(p["lugar"] for p in faltan):
            items = [f"{p['nombre']}{marca(p)}" for p in faltan if p["lugar"] == lugar]
            out.append(f"{lugar}: " + " · ".join(items))
        dudosos = [p for p in productos if p.get("rol") == "rotacion"
                   and es_dudoso(p, dias(p.get("estado_desde"), hoy))]
        if dudosos:
            out.append("\n# a confirmar (máx 5 a la ❓ del viernes, los más viejos primero)")
            out.append(" · ".join(p["nombre"] for p in dudosos[:8]))
        return "\n".join(out)

    if para == "chefcito":
        piso = [p for p in productos if p.get("origen") == "cocinado"]
        vencidos = [p for p in piso if p["estado"] != "disponible"
                    or es_dudoso(p, dias(p.get("estado_desde"), hoy))]
        hay = [p for p in productos if p["estado"] == "disponible"
               and p.get("origen", "comprado") == "comprado"]
        return "\n".join([
            f"# piso de comida lista a reponer cocinando ({len(vencidos)}/{len(piso)})",
            " · ".join(p["nombre"] for p in vencidos) or "—",
            f"\n# ingredientes disponibles ({len(hay)})",
            " · ".join(p["nombre"] for p in hay),
        ])
    raise SystemExit(f"consumidor desconocido: {para}")


def main():
    productos = json.loads((BASE / "productos.json").read_text())["productos"]
    md = render(productos, date.today())
    (BASE / "Productos.md").write_text(md)
    print(f"Productos.md regenerado: {len(productos)} productos")


def demo():
    hoy = date(2026, 8, 10)
    assert dias("2026-08-10", hoy) == 0 and dias(None, hoy) is None
    viejo = {"estado_desde": "2026-06-01", "tolerancia_dias": 3}
    md = render([
        {"nombre": "Fresco", "lugar": "Feria", "estado": "disponible", "rol": "rotacion",
         "estado_desde": "2026-08-09", "tolerancia_dias": 3},
        {"nombre": "Viejo", "lugar": "Feria", "estado": "agotado", "rol": "rotacion", **viejo},
        {"nombre": "Sal", "lugar": "Feria", "estado": "disponible", "rol": "constante", **viejo},
        {"nombre": "Azafrán", "lugar": "Feria", "estado": "disponible", "rol": "esporadico", **viejo},
        {"nombre": "Sin fecha", "lugar": "Feria", "estado": "disponible", "rol": "constante"},
        {"nombre": "Fantasma", "lugar": "Coeco", "estado": "pedido", "urgencia": "alta",
         "rol": "rotacion", "estado_desde": "2026-06-01", "tolerancia_dias": 5},
    ], hoy)
    assert "| 🟢 | Fresco | 🔄" in md, "fresco no debe salir dudoso"
    assert "| 🔴**?** | Viejo | 🔄" in md, "lo que rota caduca a los tolerancia_dias"
    assert "| 🟢 | Sal | 🔁" in md, "un constante NO caduca por tiempo, aunque sea viejo"
    assert "| 🟢 | Azafrán | 🎲" in md, "un esporádico tampoco caduca por tiempo"
    assert "| 🟢**?** | Sin fecha | 🔁" in md, "nunca registrado = dudoso incluso si es constante"
    # pedido + dudoso = pedido fantasma; ⚠️ es urgencia alta, señal aparte
    assert "| 📦**?** ⚠️ | Fantasma | 🔄" in md, "pedido vencido dudoso + urgente"
    assert md.count("## Feria") == 1 and "## Coeco" in md, "una sección por lugar"

    prods = [
        {"id": "a", "nombre": "Pepino", "lugar": "Feria", "estado": "agotado",
         "rol": "rotacion", "origen": "comprado", "urgencia": "alta", **viejo},
        {"id": "b", "nombre": "Brócoli", "lugar": "Feria", "estado": "agotado",
         "rol": "esporadico", "origen": "comprado", **viejo},
        {"id": "c", "nombre": "Yogur casero", "lugar": "Cocina", "estado": "agotado",
         "rol": "constante", "origen": "cocinado", **viejo},
        {"id": "d", "nombre": "Sal", "lugar": "Feria", "estado": "disponible",
         "rol": "constante", "origen": "comprado", "estado_desde": "2026-08-10",
         "tolerancia_dias": 30},
    ]
    comp = proyeccion(prods, hoy, "compras")
    assert "Pepino ⚠️" in comp, "lo que falta va con su urgencia"
    assert "Brócoli" not in comp, "un esporádico no entra a la lista"
    assert "Yogur casero" not in comp, "un cocinado NUNCA entra a la lista de compras"
    chef = proyeccion(prods, hoy, "chefcito")
    assert "Yogur casero" in chef, "el piso a reponer va a Chefcito"
    assert "Sal" in chef, "lo disponible es lo que se puede cocinar"
    assert len(comp) < len(json.dumps(prods)), "la proyección tiene que pesar menos que el store"
    print("demo OK")


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        demo()
    elif "--para" in sys.argv:
        prods = json.loads((BASE / "productos.json").read_text())["productos"]
        print(proyeccion(prods, date.today(), sys.argv[sys.argv.index("--para") + 1]))
    else:
        main()
