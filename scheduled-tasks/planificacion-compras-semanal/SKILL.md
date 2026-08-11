---
name: planificacion-compras-semanal
description: Viernes 20h — paso 2 de 2, arma y manda el plan de compras de la semana (después de la ventana de cambios del menú)
---

Trabajás en ${VAULT_ROOT}. **Este es el paso 2 del viernes.** El paso 1 (`planificacion-menu-semanal`, 2h antes) mandó el menú como PROPUESTA y abrió una ventana para pedir cambios.

**Paso 0 — chequeá si el menú quedó aprobado.** Mirá `~/.hestia/pending-menu-review.json`:
- **Ya no existe** → la usuaria contestó y el menú está publicado. Seguí normal.
- **Todavía existe** → la ventana venció sin respuesta. Leé su campo `menu`, publicalo vos, borrá el archivo, y **aclaralo en una línea al final del mensaje** ("cargué el menú sin tu confirmación, no llegaste a contestar — cambialo cuando quieras"). **El silencio no frena la lista**: una lista que no sale porque nadie contestó es peor que una lista aproximada.

Si el módulo cocina no está activo, saltá el paso 0 y armá la lista igual.

Ejecutá la skill `/compras` en modo lista (`.claude/skills/compras/SKILL.md`, motor en `vault/Projects/Compras/instrucciones.md`). Empezá por la proyección — `python3 tools/compras/regenerar-productos-md.py --para compras` — no por el catálogo entero. Armá el **PLAN DE SEMANA**, no la lista de un solo día: 🔴 comprá ahora · 🟡 plan por día cruzando cada ítem con el mapa de días · ❓ "¿Sigue faltando?" (máx 5, numerada, solo los `dudoso` de rol `rotacion`) · 🟢 ya tenés. Descuentos verificados contra `vault/Projects/Compras/Descuentos y medios de pago.md`; los ⚠️ sin confirmar van condicionales.

Autonomía de ejecución (sección homónima de `instrucciones.md`): (a) **VIGÍA DE PRECIOS** — todo precio relevado se persiste en `productos.json` (`precio_referencia` + `precio_verificado`); suba ≥25% contra el último registrado → línea de alerta. (b) **LINKS** — cada ítem online lleva su link directo; si no está en `productos.json`, buscalo y guardalo ahí. (c) **DRAFTS** — si un comercio que se pide por mensaje está vencido por frecuencia y no es dudoso, incluí el pedido ya redactado listo para reenviar; si es conjunto con otras personas, armalo completo usando el campo `persona`.

Antes de mandarlo (Nivel 2 del `vault/Projects/Sistema/Contrato de autonomía.md`): pasá el plan por el subagente **la-contadora** (Task tool, `subagent_type: "la-contadora"`) con SOLO el plan y el total estimado. Incluí su veredicto de 1 línea al final, **sin editar el plan en base a eso** — es información para la usuaria, no un bloqueo.

Al terminar, mandá el plan + el veredicto: `${VAULT_ROOT}/tools/hestia-bot/send.sh "<el plan + veredicto>"`. Si Telegram falla, el plan queda como resultado de esta task. **No preguntes nada — decidí**; la usuaria corrige cuando compra.
