---
categories: [project-brief, index]
subjects: [sistema, automatizacion, rutina]
status: active
nivel: v1.5
---

# Sistema — el sistema operativo de vida

> ⚠️ **Implementación de referencia.** Estos docs (ritmo semanal, comercios/descuentos,
> rutinas, playlist, formato de resúmenes) traen el ejemplo real de la autora. **Funcionan
> tal cual, pero están para que los adaptes a tu vida** — cambiá el ritmo, tus comercios, tus
> señales. Los IDs de Notion y preferencias no se editan acá: van en `config.md`.

**North star** (ejemplo): sacar la carga mental de lo mundano, disfrutar sin que abrume. El sistema evoluciona una mejora por semana hasta ser irreconocible. Poné el tuyo.

## Arquitectura — un Agentic OS

Modelo completo en [[Agentic OS PRD]]: **sensores** (capturan sin esfuerzo) → **kernel** (decide) → **actuadores** (se presentan solos). El principio: el sistema es push, no pull — aparece en el momento de decisión con una acción ya decidida.

- **iPhone/Watch = la compuerta.** [[Morning Gate]] (Screen Time + Focus + trampa) y Atajos ([[Atajos Apple]]) — el launcher "OS" es el único botón de entrada.
- **Obsidian (este vault) = la mente.** Sistemas, conocimiento, instrucciones de agentes, señales diarias (`Raw/life-signals/`). Todo agente opera leyendo estas notas.
- **Notion = el manager (GTD).** Ejecución: base Proyectos (`collection://{{PROYECTOS_COLLECTION_ID}}`), base Tareas (`collection://{{TAREAS_COLLECTION_ID}}`, con Due → aparece en Notion Calendar; tags de contexto: ⏲️ -5 mins, 🪫 Low Batery, 💻 Compu, 🏙️ Fuera de casa), y tu Journal de objetivos del año + la base Habits (`collection://{{HABITS_DB_ID}}`: las páginas Daily con mood y hábitos) + la base Reflections (`collection://{{REFLECTIONS_COLLECTION_ID}}`: weekly, monthly, quarterly, yearly).
- **Cloud** (tareas programadas de Claude): el kernel que empuja — pulso 7:30, plan 21:30, y las [[Señales de riesgo]] que se re-chequean a diario.
- **Datos de cuerpo**: **MCP health-auto-export** (sueño/ciclo/entrenos/medicación en vivo desde el iPhone, [[Atajos Apple]] §5 — Hestia estima la fase del ciclo sin preguntar; seguís cargando en Salud como siempre), **Peak Calendar** (curva de energía, conector de calendar), Strava.
- **Telegram = la boca de Hestia**: el mensaje de la mañana, las alertas, y todo lo que la usuaria le cuente ("compré…", "tomé…", "qué hago"). Setup en `tools/hestia-bot/SETUP.md`.

## Las piezas

| Pieza | Se dispara | Qué hace |
|---|---|---|
| **[[Mañana Hestia]]** | Telegram 8:30, solo | el día decidido: energía predicha (ciclo+sueño+Peak), las ≤3 ordenadas, lo que toca hoy, UNA señal si hay. **Escribe el Daily en Notion Reflections** (la página abierta en el home — el actuador persistente). Lunes: invita a planificar la semana. Botones de check-in opcionales — jamás insiste |
| **[[Morning Gate]]** | al despertar (Downtime) | bloquea IG/WhatsApp hasta 09:30, cuerpo antes que mente |
| **hestia-bot** | cuando le escribís | menú "/" con todas las piezas: `/ahora`, `/hoy` (vistazo), `/planificar` (tareas por Telegram → Notion), `/compras`, `/chefcito`, `/revision`, `/finanzas` (3 números). Texto libre: "compré…", "tarea: …", "qué hago", re-enganche — Telegram, `tools/hestia-bot/` |
| **`/ahora`** | "qué hago" (bot o acá) | UNA acción física de ≤5 min — Hestia piensa el next, vos ejecutás. Modo cocina incluido |
| `/planificar` | lunes (invitado por el tick) o cuando haga falta | brain-dump (chat o Telegram) → tareas estimadas con Due en Notion |
| `/compras` | viernes 18h, solo | plan de compras de la semana por día y canal, veredicto de la-contadora, enviado por Telegram + modo registrar |
| `/chefcito` | viernes (menú) y domingo (prep) | planifica la semana dimensionada contra tu estructura de comidas (demanda vs. porciones) y ejecuta el bloque de prep, incluido el piso de comida lista |
| `/revision` | **viernes 17h**, solo | cierre de semana con intención: weekly reflection guiada (→ página en Reflections + Mood average de Apple Health), predicho vs. reportado, ledger, racha sin scroll, 1 mejora |
| `monthly-reflection` | día 1, solo | métricas del mes automáticas (mood×ciclo×sueño×entrenos, contextual) + planificación guiada → página Monthly en Reflections |
| `/cierre-finanzas` | día 5, solo | análisis mensual + tracker 3 números ([[../Finanzas/Plan|Plan]]) |

Las 5 tareas programadas corren en la Mac (app de Claude abierta); si estaba dormida, corren al despertar — deuda cero. El bot es un proceso aparte (LaunchAgent): no necesita la app, solo la Mac despierta.

## Ritmo semanal

- **Todos los días**: 8:30 mensaje de la mañana + Daily armado en Notion (solo, con datos de salud en vivo) · pomodoros con micro-tarea de casa en el descanso de 5'.
- **Lunes**: el tick invita a **planificar la semana** (brain-dump por Telegram → `/planificar`).
- **Martes**: micro-prep — bajar del freezer lo del día de cocina + chequear verduras (2', lo recuerda `/ahora`).
- **Miércoles**: día de quien ayuda en casa — cocina, lavado semanal, limpieza profunda (lista fija en [[../Casa/README|Casa]]).
- **Viernes 17h**: `/revision` — cierre de semana con intención (weekly reflection → Notion). **18h**: el plan de compras de la semana llega solo por Telegram.
- **Sábado**: compras presenciales (el día de descuento del canal principal) · registrar la compra (`/compras` modo registrar). El finde es para procesar, no para planificar.
- **Domingo**: `/chefcito` — bloque de prep de la semana.
- **Día 1 del mes**: `monthly-reflection` (métricas + plan del mes). **Día 5**: `/cierre-finanzas`.

## Reglas del sistema

1. **Máximo 3 tareas por día.** Lo demás es mentira piadosa que después pesa.
2. **Toda estimación se multiplica ×1.5** antes de agendarse.
3. **WIP = 1-2 proyectos en foco.** El resto espera en Paused sin culpa (ver [[Triage Notion 2026-07]]).
4. **Micro-tareas de casa viven en los descansos de pomodoro**, nunca como montaña propia.
5. **Toda tarea nueva necesita próxima acción física** ("llamar a X", no "resolver Y"). Si no la tiene, no entra.
5b. **Ningún accionable se queda solo en un .md.** Si de cualquier charla, análisis o skill sale algo con próxima acción física clara, se sugiere cargarlo a Notion ahí mismo (vía `/planificar`) — no hace falta esperar a `/revision` ni que la usuaria lo pida explícito.
6. **El sistema nunca reprocha.** Semana caída = se retoma donde estaba, deuda cero.
7. **Todo dato nuevo se persiste en el vault** (productos, frecuencias, links, aprendizajes) — el sistema no pregunta dos veces lo mismo.
8. **Tokens**: manual obligatorio en [[Raw/2026-07-13 manual-modelos-claude|Raw]] — barato primero, exploración en subagentes Haiku, effort calibrado.

## Gamificación

- El sistema tiene **nivel** (frontmatter `nivel:` de esta nota): sube 0.1 con cada mejora semanal.
- `/revision` cierra con **wins de la semana** (lo cumplido, lo que se movió, la racha de pulsos atendidos) — progreso visible, presión invisible.
- Mood del Journal + Strava + cumplimiento = el tablero real de cómo viene la vida, no solo las tareas.

## Cuando el sistema se cae

Va a pasar. El protocolo es uno solo: abrir Claude, decir "me caí del sistema", y el sistema propone el re-enganche mínimo (1 pulso + 1 micro-tarea). Nada de ponerse al día con lo acumulado.

## Changelog

- **2026-08-11 · v1.5 — La cocina deja de planificar contra estado supuesto** — la causa
  raíz de casi todos los errores del módulo cocina era que el sistema "recordaba" que
  había algo cuando lo único que sabía es que **hubo**. Nuevo
  [[Modelo de estado de la cocina]] con el principio que ordena todo: **nunca inferir
  "disponible", solo se infiere hacia abajo.** `productos.json` pasa de un campo de stock
  en texto libre a una **máquina de estados** (`estado` + `estado_desde`, transiciones con
  dueño único) más tres dimensiones que resuelven problemas distintos: **`dudoso`** se
  calcula y no se guarda (es el disparador de la pregunta semanal); **`rol`**
  (`constante`/`rotacion`/`esporadico`) define a qué velocidad envejece el dato y si un
  `agotado` entra a la lista — un `esporadico` no se compra porque falte, sino si una
  receta lo pide; **`origen`** (`comprado`/`cocinado`) hace que un preparado recurrente sea
  un producto que se repone **cocinando**, así "que siempre haya algo sano para picar" deja
  de ser una intención y pasa a ser un estado con vencimiento. La planificación usa
  **commit/rollback**: el plan declara qué consume y no aplica nada hasta que la tarea
  llega a Done. Y el plan semanal se **dimensiona**: declara cuántas tomas necesita la
  semana y cuántas porciones producen los bloques, con la regla de que **producción ≥
  demanda** antes de darlo por bueno — un plan que cubre una sola comida al día se queda
  corto sin que nadie se dé cuenta. Dos scripts nuevos con self-check `--demo`:
  `regenerar-productos-md.py` (genera la vista, deriva `dudoso`, y **proyecta** lo mínimo
  que cada agente necesita en vez de que lea el catálogo entero) y `cobertura.py` (lee solo
  el frontmatter `funcion:` para decir qué cubre el menú y qué le falta). **`/setup` ahora
  entrevista** a quien active el módulo cocina sobre **su** forma de armar el menú y
  reescribe el template con esa estructura: el modelo que trae el repo es un ejemplo, no
  una doctrina. El viernes se parte en dos tareas
  (`planificacion-menu-semanal` → `planificacion-compras-semanal`, que reemplazan a
  `compras-viernes`): la lista sale del menú, así que primero se decide qué se come y se
  abre una **ventana de cambios** — pero **el silencio no frena la lista**, se publica y se
  aclara. Nuevo [[../Compras/Patrones]] con el método para minar tus resúmenes bancarios y,
  sobre todo, con el **punto ciego**: lo que pagás en efectivo o por transferencia no
  aparece en ninguna tarjeta, así que ahí tu registro es la única fuente de verdad.
- **2026-07-17 · v1.4.2 — Ejecución sin esperar a la usuaria** — el techo no se mueve
  (Hestia nunca paga), pero todo lo previo al botón ahora es del sistema:
  **carrito armado** (interactivo: carrito real en el browser; programado: link
  directo por producto, y los links se guardan en productos.json — nunca se
  busca dos veces), **vigía de precios** (cada relevamiento del viernes persiste
  `precio_referencia`+`precio_verificado`; suba ≥25% → alerta en el plan),
  **drafts de pedidos** (los comercios que se piden por mensaje salen redactados
  y listos para reenviar cuando el ciclo vence), y **cierre financiero
  automático**: el tick 8:30 detecta el set completo del mes en Resumenes/
  (según los `expected_files` de config) y corre /cierre-finanzas solo — avisa solo si hay anomalía; set
  incompleto >1 día → recordatorio de qué falta; "cerrá con lo que hay" por
  Telegram → ruta nueva del bot. También: bot.py ya no bloquea (thread por
  mensaje + acuse de recibo "⏳" inmediato — antes un /ahora lento lo dejaba
  sordo 10+ min; la Mac dormida sigue siendo la única sordera real). Adenda
  misma noche, pedida por la usuaria: **carrito de la mañana** — el tick 8:30, tras
  mandar el día, agrupa lo pendiente por canal y arma carrito si hay urgente
  (hoy, aunque pierda descuento) o si hoy es el día de descuento del canal con
  ≥2 ítems (consolidación); sin sesión iniciada en el comercio → links directos.
- **2026-07-16 · v1.4.1 — Compras autónomas** — descuentos reverificados online
  contra el sitio de cada banco/billetera (uno había muerto, otro estaba mal
  atribuido, otro sin renovación publicada → quedan marcados ⚠️ y se usan
  condicionales). Nuevo [[../Compras/Patrones|Patrones]]: patrones reales
  minados de los resúmenes bancarios (frecuencia y gasto típico por comercio) y
  un **punto ciego** que conviene conocer: los comercios que se pagan en
  efectivo o por transferencia **no aparecen en ninguna tarjeta** → ahí el modo
  registrar por Telegram es la única fuente de verdad. Motor de compras con
  **mapa de días** (urgente → hoy por el canal rápido; reponer → al día de
  descuento del canal; ir pensando → se acumula), **regla de staleness**
  (estado sin registro reciente = dudoso → sección "¿Sigue faltando?" del
  viernes, no infla urgentes) y salida como
  **plan de semana** por día/canal. `compras-viernes` emite el plan; el tick
  8:30 avisa si HOY es el día del canal de algo urgente confirmado. Verificado
  la-veterana: PASS.
- **2026-07-16 · v1.4 — El bot madura + Reflections vuelven** — menú "/" en Telegram
  con todas las piezas; tareas por Telegram (`tarea: …` → `/planificar` → Notion,
  decisión del consejo: no migrar nada, la fricción era la carga, no el lugar);
  el tick escribe el **Daily en Notion Reflections** (el actuador persistente del
  home); `/revision` pasa a **viernes 17h** con la weekly reflection guiada
  (finde para procesar, lunes para planificar — invitado por el tick);
  `monthly-reflection` nueva (día 1: mood×ciclo×sueño×entrenos contextual, sin
  tracking manual — reemplaza el CSV a mano para GPT); Mood automático desde
  Apple Health (automation "Mood" → health-receiver, verificada); calendarios
  como contexto (Peak dinámico gana sobre "Rutina" estático); bot se auto-reinicia
  tras 10 errores de red seguidos (fix del socket zombi).
- **2026-07-15 · v1.3 — Consejo de subagentes** — 4 agentes con criterio estable
  (la-contadora, la-entrenadora, la-veterana, la-abogada-del-diablo), [[Contrato de autonomía]]
  formal (3 niveles + techo permanente), [[Trust ledger]] (tiers
  watch→queue→auto), heurística de energía formalizada en [[Energia]] (parámetros
  ajustables, ya no vive inline en el prompt del tick). `compras-viernes` pasa por
  la-contadora antes de mandar la lista; `weekly-reflection` administra el ledger
  y verifica la mejora semanal con la-veterana. [[../Wellness App/README|Wellness
  App]] reencuadrada: incubando en Hestia (laboratorio n=1), no se construye app.
- **2026-07-15 · v1.2 — Hestia 🏛️** — el sistema pasa de preguntar a encargarse: bot de Telegram (`tools/hestia-bot/`), [[Mañana Hestia]] 8:30 con el día decidido y energía predicha (ciclo+sueño+Peak, input opcional), **MCP health-auto-export** (sueño/ciclo/medicación en vivo, sin Atajos ni reportar nada), 4 tareas programadas reales, 3 reglas de autonomía (nunca paga/borra/publica). Eliminados: pulso con preguntas obligatorias, plan nocturno interactivo, y el log manual de suplementos por chat. Consejo de subagentes + trust ledger → roadmap v1.3 del [[Agentic OS PRD|PRD]].
- **2026-07-15 · v1.1** — Agentic OS: [[Agentic OS PRD|PRD]], [[Morning Gate]] (3 capas), [[Señales de riesgo]] (6 predicados diarios), pipeline life-signals (Atajo → iCloud Drive → vault), copiloto `/ahora` con [[../Casa/Rutinas|Rutinas]] encadenadas, launcher "OS", Peak Calendar como sensor de energía, pulso 7:30 adaptativo.
- **2026-07-13 · v1.0** — Sistema inicial: 5 skills, 5 tareas programadas, Finanzas/Plan, Casa, Cuerpo Sano, política de tokens, triage de Notion.
