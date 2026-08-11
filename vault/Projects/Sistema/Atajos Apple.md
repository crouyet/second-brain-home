---
categories: [permanent-note]
subjects: [sistema, atajos, celular]
status: active
---

# Atajos de Apple — la interfaz física del sistema

Specs para armar/revivir cada atajo (5-10 min c/u en la app Atajos). El criterio: **un tap desde el celu mata la fricción de arranque**, que es donde todo muere.

## 1. Pomodoro doméstico ⭐ (revivir el que ya tenés)

El que tenés + un agregado: **el descanso trae una micro-tarea, no descanso vacío**.

1. Al iniciar: timer 25' (tu atajo actual).
2. Al sonar: notificación con **una** micro-tarea de esta lista rotativa (acción "Obtener elemento de lista" → "Elegir aleatorio"):
   - Platos: solo lo que entra en 5'
   - Tender / doblar una tanda de ropa
   - Despejar la mesada
   - Mesa/escritorio: reset de superficie
   - Sacar la basura
   - Regar plantas
3. Timer 5' y vuelta al trabajo. La tarea que no terminó en 5' **se abandona sin culpa** — el próximo descanso sigue.

## 2. Pulso *(absorbido por el launcher — ver §8)*

~~1 acción: "Abrir app" → Claude, con texto "Dame el pulso de hoy".~~ Ahora es una opción del menú del launcher **OS** (§8). Si ya lo armaste suelto, no hace falta borrarlo — pero el widget de la pantalla de inicio es el launcher.

## 3. Registrar compra 🎤

1. "Dictar texto" (decís: "compré sésamo en <comercio> 3200, kombucha en <otro>...").
2. "Agregar a nota" → nota "Compras por registrar" en Notas de Apple.
3. En la próxima sesión de `/compras`, Claude vacía esa nota al vault (`ultima_compra`, precios, stock). Cero fricción en el momento, cero dato perdido.

## 4. Log de suplementos 💊 — no hace falta ningún atajo

Si cargás tus tomas en Salud → Medicamentos, con eso alcanza: el MCP health-auto-export (§5) lo lee de ahí, en vivo. No hace falta ningún atajo extra ni contarle al bot "tomé X" — sería redundante.

## 5. Health Auto Export MCP 🩺 — el sensor de cuerpo de Hestia

Reemplaza al plan original de Atajos + iCloud (Shortcuts no puede leer medicamentos, ni en iOS 26 — verificado). **Health Auto Export Premium** (US$5,99/año) da dos caminos, complementarios:

### Vía confiable — health-receiver (REST API push, corre solo en segundo plano)

La app manda (POST) los datos sola cuando el iPhone se desbloquea, **sin necesitar la app abierta** — a diferencia del MCP en vivo. Setup completo (3 automations en la app + qué headers poner): **`tools/health-receiver/SETUP.md`**. El receptor ya corre en la Mac como servicio (`tools/health-receiver/`), guarda todo en `vault/Raw/health/*.json`. Esta es la fuente principal que lee [[Mañana Hestia]].

### Vía bonus — MCP en vivo (tiempo real, pero necesita la app abierta)

Servidor MCP propio corriendo en el iPhone: Hestia puede consultar sueño/ciclo/medicación en vivo si la app está abierta en ese momento.

**Setup (una vez):**
1. En la app → Server → activar el server MCP, dar los permisos de Salud que pida.
2. "AI Client" → `Claude Code (JSON)` → copiar.
3. En la Mac: `cd ${VAULT_ROOT} && pbpaste > .mcp.json` (Universal Clipboard sincroniza el copiado del iPhone). El bearer token queda ahí — **ese archivo tiene un secreto, no se comparte ni se sube a git**.
4. Confirmar que el JSON pegado tiene `mcpServers.health-auto-export` con `url` y `headers.Authorization`.

**Limitación conocida**: el server MCP solo responde con la app abierta y en primer plano. Por eso existe la vía confiable de arriba — no hace falta abrir nada para que Hestia tenga datos. La IP del server (`http://<TU-IP-LAN>:9000/mcp` al momento de configurarlo) puede cambiar si el router reasigna DHCP.

Se descartó usar el "Sync to Mac"/AutoSync de la app: formato binario propio (.hae, lzfse) y no incluye ciclo ni medicamentos.

Suplementos ya NO se registran contándole al bot — vienen automático de acá. *(App nativa propia con HealthKit: roadmap v2.2 del [[Agentic OS PRD|PRD]], baja prioridad con esto andando.)*

## 6. Pulso mínimo de mañana 🌅 *(DEPRECADO — lo reemplazó el bot de Telegram)*

**No hace falta armar este atajo.** El check-in ahora son los 3 botones opcionales (🪫🔋⚡️) del mensaje de la mañana de Hestia en Telegram — cero configuración, y si no los tocás no pasa nada. La spec de abajo queda solo por si algún día hace falta el fallback sin Telegram.

<details><summary>Spec original (fallback)</summary>

1. Acción **"Fecha actual"** → encadenale **"Formatear fecha"** con formato personalizado `AAAA-MM-dd` (ISO). Tocá el resultado y nombralo `FechaISO` — **una sola vez**, se reusa abajo en el JSON y en el nombre del archivo. Esto evita el bug de que la fecha del contenido y la del nombre salgan con formatos distintos si tu iPhone está en español.
2. Tres acciones **"Elegir del menú"** encadenadas (un tap cada una — nombrá cada variable de salida al toque: `Energia`, `Cuerpo`, `Mental`, para no perderte después):
   - Energía: `baja` / `media` / `alta`
   - Cuerpo: `frío` / `hambre` / `dolor-cansancio` / `ok`
   - Mental: `clara` / `dispersa` / `ansiosa` / `pesada`
3. Acción **"Texto"** que arma el JSON (schema exacto en `vault/Raw/life-signals/README.md`) — insertá `FechaISO`/`Energia`/`Cuerpo`/`Mental` con el botón azul de variables, no las tipees a mano:
   `{"date":"[FechaISO]","time":"[Hora actual, formato HH:mm]","energia":"[Energia]","cuerpo":"[Cuerpo]","mental":"[Mental]","scroll_intents":0}`
4. Acción **"Guardar archivo"** → **elegí "iCloud Drive"** en el picker de ubicación (si no aparece la carpeta `life-signals`, creála una vez a mano desde la app Archivos, después el atajo la encuentra sola) → nombre de archivo con la **misma variable**: `[FechaISO]-morning.json` → **"Preguntar antes de reemplazar": OFF** (si no, se traba pidiendo confirmación cada mañana).
5. Si energía=`baja` o cuerpo=`frío`: acción "Mostrar notificación" con la secuencia corporal: *"Abrigo → agua → suplemento → comida mínima → luz 3-5 min. Una por vez."*

**Gotchas más comunes de este atajo** (si se traba, suele ser uno de estos):
- El "Elegir del menú" por defecto no crea variable propia — tenés que tocar el resultado y ponerle nombre, si no la acción de Texto no lo encuentra en la lista de variables mágicas.
- "Guardar archivo" a veces ofrece "Guardar PDFs" por error si el input no es texto — asegurate de que lo que entra ahí sea la salida de la acción "Texto" (JSON), no el menú directo.
- Fecha con formato regional: por eso el paso 1 usa "Formatear fecha" explícito en vez de confiar en el default de "Fecha actual".

</details>

## 7. Trampa IG/WhatsApp 🪤 (2 automations, ~5 min c/u)

Sensor, no barrera (la barrera es Screen Time — [[Morning Gate]] capa 1).

- Automatización personal: **"Al abrir Instagram"** (y otra igual para WhatsApp), "Ejecutar inmediatamente":
  1. **Si** hora actual < 09:30:
  2. "Agregar a texto/archivo": suma una línea `[fecha hora] intento IG` al archivo `life-signals/scroll-intents.txt` de iCloud Drive.
  3. "Mostrar alerta": **"No es momento. Primero cuerpo."**
  4. "Ejecutar atajo" → Pulso mínimo (§6), si todavía no se hizo hoy.

## 8. Launcher "OS" 🧭 — un botón para todo (~10 min)

El punto de entrada único al sistema. Widget en pantalla de inicio + Action Button + complicación del Watch.

Una acción **"Elegir del menú"**; cada opción = "Abrir app" → Claude con texto precargado:

| Opción | Texto que manda |
|---|---|
| 🧭 ¿Qué hago? | `/ahora` |
| 🌅 Pulso | `Dame el pulso de hoy` |
| 🍳 Cocinar | `/ahora cocinar` |
| 🛒 Registrar compra | "Dictar texto" → `/compras registrar: [dictado]` |
| 🧠 Planificar | "Dictar texto" → `/planificar [dictado]` |
| 🆘 Me caí | `me caí del sistema` |

Regla: **todo lo conversacional entra por acá**. Los sensores (§6 pulso, §7 trampa, §5 health) corren solos — no son conversación.
