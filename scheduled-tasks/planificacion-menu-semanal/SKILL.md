---
name: planificacion-menu-semanal
description: Viernes 18h — paso 1 de 2, planifica el menú de la semana y lo manda como PROPUESTA, con ventana de cambios
---

Trabajás en ${VAULT_ROOT}. **Este es el paso 1 del viernes**; el paso 2 (`planificacion-compras-semanal`, 2h después) arma la lista de compras. Están separados a propósito: la lista sale del menú, así que primero se decide qué se come y se da tiempo real para pedir cambios.

Solo corre si la usuaria activó el módulo cocina y planifica por semana (sección `## Chefcito` de `vault/Projects/Sistema/config.md`, campo `plans_weekly`). Si no está o es `false`, no hagas nada.

Ejecutá `/chefcito` en **modo planificación semanal** (`.claude/skills/chefcito/SKILL.md`). Ese modo ya hace todo: cierra el plan anterior (commit/rollback de los efectos declarados), calcula la demanda de la semana, elige las recetas, declara porciones, chequea que **producción ≥ demanda**, y escribe el plan en `vault/Projects/Chefcito/Planes Semanales/Plan-semana-<fecha>.md`.

**Mandá el menú como PROPUESTA por Telegram y NO publiques nada todavía**: `${VAULT_ROOT}/tools/hestia-bot/send.sh "<el menú + '¿cambiás algo? tenés hasta las 20h'>"`. Dejá la marca `~/.hestia/pending-menu-review.json` con `{"date": "<hoy ISO>", "ts": <epoch>, "menu": "<el menú tal como se lo mandaste>"}` — el paso 2 la lee para saber si hubo respuesta.

Si la usuaria quiere cambios, contesta por Telegram con `/chefcito <lo que quiere cambiar>`: eso re-invoca la skill, rehacés la propuesta, la volvés a mandar y actualizás la marca. Si aprueba, publicás el menú y **borrás la marca**.

> **Captura automática de la respuesta**: el bot del template rutea los mensajes que empiezan con `/chefcito`, así que ese es el camino que funciona sin tocar nada. Si querés que capture también un "dale" suelto dentro de la ventana, hay que agregarle esa ruta a `tools/hestia-bot/bot.py` — es opcional, el flujo cierra igual por el paso 2.

**No corras `/compras`**: lo hace el paso 2, para darle tiempo real a contestar.
