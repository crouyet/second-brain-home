# hestia-bot — setup (una vez, ~10 min)

El canal de Telegram de Hestia: te manda el día decidido cada mañana y le podés escribir libre ("compré…", "tomé magnesio", "qué hago").

## 1. Crear el bot (2 min)

Ya creado ✓ — el bot es **[@Hestia_os_bot](https://t.me/Hestia_os_bot)**.

1. En Telegram, hablale a **@BotFather** → `/newbot` → nombre: `Hestia` → username: algo tipo `hestia_cami_bot`.
2. Copiá el **token** que te da.
3. **Importante**: hablale a tu bot nuevo (cualquier "hola") para que exista el chat.

## 2. Configurar (2 min)

```bash
mkdir -p ~/.hestia
cp tools/hestia-bot/telegram.env.example ~/.hestia/telegram.env
# editá ~/.hestia/telegram.env: pegá el TOKEN
TELEGRAM_TOKEN=<tu token> tools/hestia-bot/whoami.sh   # te muestra tu chat_id
# completá CHAT_ID en el env
chmod 600 ~/.hestia/telegram.env
```

El token vive SOLO en ese archivo — nunca en el vault ni en un chat.

`CHAT_ID` tiene que ser el de tu chat 1-a-1 con el bot, **nunca un grupo**: el bot ignora todo lo
que no venga de ese chat, así que ese número es el único auth que hay. En un grupo, cualquier
miembro le hablaría a Claude con tu misma autoridad.

## 3. Arrancar (1 min)

```bash
tools/hestia-bot/install.sh
```

Probá: mandale "hola" al bot → tiene que responder.

## 4. Que la Mac esté despierta a las 8:30 (1 min)

```bash
sudo pmset repeat wakeorpoweron MTWRFSU 08:25:00
```

Si la Mac durmió igual, el mensaje sale cuando despierte — deuda cero.

## Qué entiende el bot

| Le escribís | Hace |
|---|---|
| `tomé magnesio` | lo loguea en life-signals/supplements.log |
| `compré sésamo 3200 en frutos are` | `/compras registrar` |
| `qué hago` | `/ahora` — te da UNA acción |
| `cocinar` | `/ahora cocinar` |
| `me caí` / `no doy más` | re-enganche mínimo, sin culpa |
| botones 🪫🔋⚡️ del mensaje de la mañana | guarda tu energía del día (opcional, jamás insiste) |
| cualquier otra cosa | Hestia general: registra o responde corto |

## Limitaciones conocidas (v1)

- Corre en la Mac: si está apagada, el bot no responde hasta que vuelva (los pendientes de Telegram llegan igual al reconectar).
- Las respuestas que usan skills tardan lo que tarda la skill (hasta ~1-2 min).
- En headless algunas skills no ven los conectores de la app (Notion/Calendar) — degradan con gracia y lo dicen.
