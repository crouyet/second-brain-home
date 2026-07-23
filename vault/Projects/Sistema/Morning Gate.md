---
categories: [permanent-note]
subjects: [sistema, morning-gate, celular]
status: active
hora_liberacion: "09:30"
---

# Morning Gate — la compuerta de la mañana

**El momento más peligroso del día**: despertar cansada, con frío, celu en la mano "por si alguien habló" → Instagram. No es falta de intención, es fricción corporal + teléfono disponible. La compuerta asume eso y pone la barrera ANTES de la fuerza de voluntad.

**Parámetros** (editables acá, son la fuente de verdad): hora de liberación **09:30** · apps bloqueadas: Instagram, WhatsApp, YouTube, Safari.

Tres capas. Ninguna sola alcanza; juntas sí.

## Capa 1 — Screen Time (la barrera REAL)

Focus no bloquea apps; Screen Time sí. Esta capa es la que aguanta el "solo un ratito".

Checklist de configuración (una vez, ~15 min):

- [ ] Ajustes → Tiempo en pantalla → **Tiempo de inactividad** (Downtime): desde tu hora de dormir hasta **09:30**.
- [ ] Activar **"Bloquear durante el tiempo de inactividad"** (el bloqueo real, no solo el aviso).
- [ ] **Siempre permitidas** → dejar SOLO: Teléfono, Mensajes, Salud, Atajos, Calendario, Reloj.
- [ ] Sacar de "Siempre permitidas" a Instagram, WhatsApp, YouTube y Safari (quedan bloqueadas hasta las 09:30).
- [ ] Comunicación durante inactividad → contactos urgentes permitidos **por llamada/SMS** (no por WhatsApp).
- [ ] Código de Tiempo en pantalla: idealmente que lo ponga otra persona, o uno que no te sepas de memoria.

## Capa 2 — Focus "Morning Gate" (la pantalla que ves)

- [ ] Ajustes → Concentración → nueva: **Morning Gate**.
- [ ] Automatización: se activa a tu hora de despertar (o al desactivar la alarma de Sueño).
- [ ] Pantalla de inicio: mostrar SOLO una página con widgets de clima, calendario (con Peak Calendar visible — ves tu curva de energía del día), salud, y el botón del **Pulso mínimo** ([[Atajos Apple]] §6).
- [ ] Silenciar notificaciones de IG y WhatsApp; permitir llamadas de favoritos.
- [ ] Compartir entre dispositivos: ON (Watch y Mac entran en modo compuerta también).

## Capa 3 — Atajo trampa (el sensor)

No es barrera: es registro + redirección. Spec en [[Atajos Apple]] §7.

- Automation "Al abrir Instagram" y "Al abrir WhatsApp": si es antes de las 09:30 → suma 1 al contador de intentos del día (life-signals), muestra "**No es momento. Primero cuerpo.**" y abre el atajo Pulso mínimo.
- Cada intento queda registrado → `/revision` los ve como dato, no como reproche.

## El Pulso mínimo (20 segundos, 3 taps)

Tres preguntas de menú, nada de tipear ([[Atajos Apple]] §6):

1. **Energía**: baja / media / alta
2. **Cuerpo**: frío / hambre / dolor-cansancio / ok
3. **Mental**: clara / dispersa / ansiosa / pesada

→ escribe `YYYY-MM-DD-morning.json` en iCloud Drive/life-signals/ (schema en `vault/Raw/life-signals/README.md`).

Suplementos se sacó de acá (sumaba fricción): vive en [[Atajos Apple]] §4, registrado en el momento de tomarlo, no como recuerdo del día siguiente.

## Regla de liberación

- Completar el pulso **libera el sistema operativo del día, no el scroll**. Las redes se abren solas a las 09:30, no antes ni por premio.
- WhatsApp tiene ventana controlada **después** del primer bloque corporal/comida/suplementos.

## Si el pulso dice energía baja o frío

NO se planifica trabajo primero. Secuencia corporal, en orden, una por vez:

1. Abrigo / calor
2. Agua
3. Suplemento si corresponde
4. Comida mínima
5. Luz + movimiento 3-5 min

Recién después, UNA tarea `⏲️ -5 mins` o `🪫 Low Batery`. El push de las 7:30 aplica esto solo.

## Capa opcional: unrot

Claude no puede controlar el iPhone — la barrera real es Screen Time. Si reactivás unrot (la tenés pausada), sumala como capa extra sobre IG: más fricción nunca sobra. Pero el sistema no depende de ella.

---

Parte del [[Agentic OS PRD]] · señales que alimenta: [[Señales de riesgo]] (morning_scroll_risk)
