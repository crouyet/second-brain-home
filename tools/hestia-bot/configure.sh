#!/usr/bin/env bash
# Setup interactivo del bot: pide el token y el chat_id, los guarda, listo.
# Uso: tools/hestia-bot/configure.sh
set -euo pipefail

mkdir -p "$HOME/.hestia"
ENV_FILE="$HOME/.hestia/telegram.env"

echo "Pegá acá el token que te dio @BotFather (click derecho > pegar, o Cmd+V) y apretá Enter:"
read -r TOKEN
if [ -z "$TOKEN" ]; then
  echo "No pegaste nada, no guardé nada. Corré el script de nuevo cuando lo tengas a mano."
  exit 1
fi

cat > "$ENV_FILE" <<EOF
TELEGRAM_TOKEN=$TOKEN
CHAT_ID=
EOF
chmod 600 "$ENV_FILE"
echo "✓ Token guardado."
echo ""
echo "Ahora andá a Telegram y mandale CUALQUIER mensaje a tu bot (ej: 'hola')."
echo "Cuando lo hayas hecho, volvé acá y apretá Enter."
read -r _

RESULT=$(curl -sS "https://api.telegram.org/bot${TOKEN}/getUpdates")
CHAT_ID=$(python3 -c "
import json
data = json.loads('''$RESULT''')
ids = []
for r in data.get('result', []):
    m = r.get('message')
    if m:
        ids.append((m['chat']['id'], m['chat'].get('first_name', '')))
if ids:
    cid, name = ids[-1]
    print(cid)
")

if [ -z "$CHAT_ID" ]; then
  echo "No encontré ningún mensaje tuyo todavía."
  echo "Fijate que le hayas escrito al bot correcto, esperá unos segundos y corré este script de nuevo."
  exit 1
fi

sed -i '' "s/^CHAT_ID=.*/CHAT_ID=$CHAT_ID/" "$ENV_FILE"
chmod 600 "$ENV_FILE"
echo "✓ Listo. Tu chat_id ($CHAT_ID) quedó guardado."
echo ""
echo "Último paso: tools/hestia-bot/install.sh"
