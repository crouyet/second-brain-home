#!/usr/bin/env python3
"""Cobertura funcional del menú de la semana: qué funciones toca y cuáles quedan sin tocar.

Lee SOLO el frontmatter `funcion:` de Recetas/*.md. Una biblioteca de 200 recetas leída
entera cuesta ~55.000 tokens; esto emite 3 líneas. Por eso lo corre un script y no el agente.

    python3 tools/chefcito/cobertura.py <slug1> <slug2> <slug3>
    python3 tools/chefcito/cobertura.py --flojas   # funciones con menos recetas en tu librería

El slug es el nombre del archivo sin `.md`. Para que sirva, tus recetas tienen que declarar
`funcion: [tag, tag]` en el frontmatter — ver las de ejemplo en Recetas/.

PISO es el piso funcional de UNA semana y **es tuyo**: editalo con lo que a vos te importa.
El default de abajo es un ejemplo razonable, no una recomendación médica.
"""
import re
import sys
from pathlib import Path

RECETAS = Path(__file__).resolve().parents[2] / "vault/Projects/Chefcito/Recetas"

# EJEMPLO — editalo con tu piso. No es "una de cada una": son las que si faltan dos
# semanas seguidas se notan. Ver vault/Projects/Chefcito/Plan-nutricional.md.
PISO = {"proteina-densa": 5, "omega-3": 2, "magnesio": 2, "antiinflamatorio": 1,
        "fibra-prebiotica": 2, "probiotico-fermentado": 1, "hierro": 1,
        "colageno-vitc": 1, "antioxidante-polifenoles": 2}


def funciones(slug):
    """Las funciones de una receta. Slug sin .md; None si no existe el archivo."""
    f = RECETAS / f"{slug}.md"
    if not f.exists():
        return None
    m = re.search(r"^funcion:\s*\[(.*?)\]", f.read_text(), re.M)
    return [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []


def cobertura(slugs):
    """{funcion: cuántas recetas del menú la aportan} + los slugs que no existen."""
    cuenta, faltantes = {}, []
    for s in slugs:
        fs = funciones(s)
        if fs is None:
            faltantes.append(s)
            continue
        for f in fs:
            cuenta[f] = cuenta.get(f, 0) + 1
    return cuenta, faltantes


def informe(slugs):
    cuenta, faltantes = cobertura(slugs)
    out = []
    if faltantes:
        out.append(f"⚠️  recetas que no existen en Recetas/: {', '.join(faltantes)}")
    cubre = ", ".join(f"{f} ×{n}" for f, n in sorted(cuenta.items(), key=lambda x: -x[1]))
    out.append(f"cubre: {cubre or '—'}")
    huecos = {f: PISO[f] - cuenta.get(f, 0) for f in PISO if cuenta.get(f, 0) < PISO[f]}
    if huecos:
        det = ", ".join(f"{f} (falta {n})" for f, n in sorted(huecos.items(), key=lambda x: -x[1]))
        out.append(f"NO llega al piso: {det}")
        out.append(f"→ la receta nueva de la semana debería apuntar a: {max(huecos, key=huecos.get)}")
    else:
        out.append("llega al piso funcional de la semana ✓")
    return "\n".join(out)


def flojas():
    """Funciones con menos recetas en toda la librería — dónde conviene sumar recetas nuevas."""
    cuenta = {}
    if not RECETAS.is_dir():
        return []
    for f in RECETAS.glob("*.md"):
        m = re.search(r"^funcion:\s*\[(.*?)\]", f.read_text(), re.M)
        for x in (m.group(1).split(",") if m else []):
            if x.strip():
                cuenta[x.strip()] = cuenta.get(x.strip(), 0) + 1
    return sorted(cuenta.items(), key=lambda x: x[1])


def demo():
    """Self-check que no depende de qué recetas tengas: usa las de ejemplo del repo."""
    assert funciones("no-existe-esta-receta") is None, "receta inexistente debe dar None"
    c, f = cobertura(["caldo-base", "inventada-xyz"])
    assert f == ["inventada-xyz"], "tiene que reportar la que no existe"
    assert c.get("proteina-densa") == 1, "caldo-base aporta proteina-densa"
    # cuenta por receta que aporta la función, no por receta total
    c, _ = cobertura(["caldo-base", "caldo-base"])
    assert all(v == 2 for v in c.values()), "dos recetas con la misma función suman 2"
    txt = informe(["caldo-base"])
    assert "NO llega al piso" in txt, "un solo plato no puede cubrir la semana"
    assert "apuntar a" in txt, "tiene que sugerir dónde apuntar"
    # sin recetas no revienta: informa el vacío
    assert "—" in informe([]), "un menú vacío se reporta, no explota"
    print("demo OK")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--demo" in args:
        demo()
    elif "--flojas" in args:
        for f, n in flojas():
            print(f"  {n:4}  {f}")
    elif args:
        print(informe(args))
    else:
        print(__doc__)
