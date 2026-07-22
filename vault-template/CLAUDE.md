# Vault

Este vault es la base de conocimiento personal de la usuaria. Si sos Claude (u otro agente), leé esto primero para saber dónde buscar y dónde escribir.

## Configuración y placeholders (IMPORTANTE)

Los skills y las scheduled-tasks usan placeholders que **resolvés desde `Projects/Sistema/config.md`**, no los edites en los prompts:
- `{{TAREAS_COLLECTION_ID}}`, `{{REFLECTIONS_COLLECTION_ID}}`, `{{HABITS_DB_ID}}`, `{{PROYECTOS_COLLECTION_ID}}` → los `collection://` de las bases de Notion.
- `${VAULT_ROOT}` → la raíz del vault (también en `~/.hestia/vault-root.env`).
- El **mapeo señal→fuente** (mood/ciclo/sueño/meds/entrenos → apple-health / manual-notion / strava / gcal) y demás preferencias también salen de `config.md`.

Si `config.md` no existe todavía, copialo de `config.example.md` y avisá que falta correr `/setup`.

## Estructura

| Carpeta | Qué es | Regla |
|---|---|---|
| `Inbox/` | Capturas rápidas, borradores, notas sin procesar | Todo lo nuevo entra acá. Se vacía procesando hacia Wiki o Projects. |
| `Raw/` | Material crudo: clippings web, transcripciones, exports | No editar el contenido original; agregar solo frontmatter. |
| `Wiki/` | Conocimiento permanente y estructurado | Notas atómicas, bien linkeadas con `[[wikilinks]]`. |
| `Projects/` | Trabajo activo, una carpeta por proyecto | Cada proyecto tiene su `README.md` con contexto y estado. |

Prioridad de lectura: el `README.md` del proyecto relevante → `Wiki/` → `Raw/`. `Inbox/` es transitorio, no es fuente de verdad.

## Frontmatter

Las notas usan YAML frontmatter para poder consultarlas con Bases:

```yaml
---
categories: [permanent-note]   # qué ES la nota (permanent-note, project-brief, clipping, draft)
subjects: [compras, salud]     # de qué TRATA
status: active                 # active | done | archived
---
```

Las notas de productos (`Projects/Compras/Productos/`) usan su propio esquema (`lugar`, `frecuencia`, `stock_actual`, etc.) — no lo cambies sin actualizar `Productos.base`.

## Sobre la usuaria

Antes de escribir en su nombre o tomar decisiones por ella, leé:

- [[Wiki/Perfil]] — quién es, visión de vida, valores, cómo trabajar con ella.
- [[Wiki/Estilo de comunicación]] — tono y voz (personal y de marca).
- [[Wiki/Carrera]] — historial profesional y objetivos.
- [[Wiki/Salud y bienestar]] — entrenamiento, ciclo, cocina, salud circulatoria.

## Proyectos activos

Índice completo en [[Projects/README]]. Principales:

- [[Projects/Compras/README|Compras]] — agente de compras inteligente (productos, descuentos, lugares).
- [[Projects/Chefcito/README|Chefcito]] — agente culinario: inventario → meal prep accionable.
- [[Projects/Wellness App/README|Wellness App]] — app gamificada por y para mujeres (en ideación).
